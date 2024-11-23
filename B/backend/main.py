import os
import sys
import psycopg2
from psycopg2 import sql
from contextlib import contextmanager
from dotenv import load_dotenv
from config_manager import ConfigManager
from logger import Logger

# Add the modules directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

class EnvManager:
    """
    A class to manage environment variables.
    """

    def __init__(self, env_file_path=".env"):
        """
        Initialize the EnvManager instance.

        Args:
            env_file_path (str): Path to the environment file.
        """
        self.env_file_path = os.path.abspath(env_file_path)

    def load_env(self):
        """
        Load environment variables from the .env file.

        Returns:
            bool: True if environment variables were successfully loaded, False otherwise.
        """
        if os.path.exists(self.env_file_path):
            load_dotenv(self.env_file_path)
            return True
        else:
            print(f"Environment file not found at {self.env_file_path}")
            return False

    def get_env_var(self, key):
        """
        Retrieve the value of a specific environment variable.

        Args:
            key (str): The key of the environment variable.

        Returns:
            str: The value of the environment variable, or None if it doesn't exist.
        """
        return os.getenv(key)

    def set_env_var(self, key, value):
        """
        Set an environment variable in the current session.

        Args:
            key (str): The key of the environment variable.
            value (str): The value of the environment variable.
        """
        os.environ[key] = value

class DatabaseManager:
    """
    A class to manage database interactions.
    """

    def __init__(self):
        """
        Initialize the DatabaseManager instance.
        """
        self.config_manager = ConfigManager()
        self.db_config = {
            "dbname": self.config_manager.get("database.db_name"),
            "user": self.config_manager.get("database.db_user"),
            "password": self.config_manager.get("database.db_password"),
            "host": self.config_manager.get("database.db_host"),
            "port": self.config_manager.get("database.db_port")
        }

    @contextmanager
    def _get_connection(self):
        """
        Context manager for obtaining a database connection.

        Yields:
            psycopg2 connection: A connection object for the database.
        """
        connection = psycopg2.connect(**self.db_config)
        try:
            yield connection
        finally:
            connection.close()

    @contextmanager
    def _get_cursor(self, connection):
        """
        Context manager for obtaining a database cursor.

        Args:
            connection (psycopg2 connection): The active database connection.

        Yields:
            psycopg2 cursor: A cursor object for executing queries.
        """
        cursor = connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def initialize_database(self):
        """
        Initialize the database with required tables.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with self._get_connection() as conn:
            with self._get_cursor(conn) as cur:
                cur.execute(create_table_query)
                conn.commit()

    def insert_user(self, username, email):
        """
        Insert a new user into the database.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.

        Returns:
            int: The ID of the newly inserted user, or None if the user already exists.
        """
        # Check if the user already exists
        select_query = "SELECT id FROM users WHERE username = %s;"
        with self._get_connection() as conn:
            with self._get_cursor(conn) as cur:
                cur.execute(select_query, (username,))
                existing_user = cur.fetchone()
                if existing_user:
                    # User already exists, return their ID
                    print(f"User with username '{username}' already exists.")
                    return existing_user[0]

        # If the user does not exist, proceed with insertion
        insert_query = """
        INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id;
        """
        with self._get_connection() as conn:
            with self._get_cursor(conn) as cur:
                cur.execute(insert_query, (username, email))
                conn.commit()
                return cur.fetchone()[0]

    def fetch_users(self):
        """
        Fetch all users from the database.

        Returns:
            list: A list of user records.
        """
        select_query = "SELECT id, username, email, created_at FROM users;"
        with self._get_connection() as conn:
            with self._get_cursor(conn) as cur:
                cur.execute(select_query)
                return cur.fetchall()

def main():
    # Initialize Logger
    logger = Logger("application.log")
    try:
        logger.info("Loading environment variables...")

        # Initialize EnvManager and load the environment variables
        env_manager = EnvManager(".env")
        if env_manager.load_env():
            logger.info("Environment variables loaded successfully.")
        else:
            logger.error("Failed to load environment variables.")
            
        # Now you can safely access environment variables
        db_username = env_manager.get_env_var("DB_USERNAME")
        logger.info(f"DB_USERNAME: {db_username}")

        # Initialize DatabaseManager without arguments
        logger.info("Initializing database...")
        db_manager = DatabaseManager()  # Corrected instantiation here
        db_manager.initialize_database()

        # Step 2: Insert User into Database
        logger.info("Inserting user into database...")
        user_id = db_manager.insert_user("johndoe", "johndoe@example.com")
        logger.info(f"Inserted user with ID: {user_id}")

        # Step 3: Fetch Users from Database
        logger.info("Fetching users from database...")
        users = db_manager.fetch_users()
        logger.info("Users in database:")
        for user in users:
            logger.info(f"User: {user}")

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print("Application encountered an error. Check logs for details.")

    logger.info("Backend integration tests completed.")

if __name__ == "__main__":
    main()
