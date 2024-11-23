import sqlite3
import hashlib
import os

class UserManager:
    def __init__(self, db_path="F:\\B\\backend\\data\\ghnet.db"):
        """
        Initialize the UserManager with a database connection.
        
        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """Initialize the users table if it doesn't already exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL
                )
            """)
            conn.commit()

    def _hash_password(self, password):
        """
        Generate a secure hash for a password using a random salt.
        
        Args:
            password (str): Plaintext password.
        
        Returns:
            tuple: (password_hash, salt)
        """
        salt = os.urandom(16).hex()
        password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
        return password_hash, salt

    def _verify_password(self, password, password_hash, salt):
        """
        Verify a password against a hash and salt.
        
        Args:
            password (str): Plaintext password.
            password_hash (str): Stored password hash.
            salt (str): Stored salt.
        
        Returns:
            bool: True if the password matches, False otherwise.
        """
        return hashlib.sha256((password + salt).encode('utf-8')).hexdigest() == password_hash

    def add_user(self, username, password):
        """
        Add a new user to the database.
        
        Args:
            username (str): Username.
            password (str): Plaintext password.
        
        Returns:
            str: Success or error message.
        """
        password_hash, salt = self._hash_password(password)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO users (username, password_hash, salt) 
                    VALUES (?, ?, ?)
                """, (username, password_hash, salt))
                conn.commit()
                return f"User '{username}' added successfully."
            except sqlite3.IntegrityError:
                return f"Error: Username '{username}' already exists."

    def authenticate(self, username, password):
        """
        Authenticate a user by verifying their credentials.
        
        Args:
            username (str): Username.
            password (str): Plaintext password.
        
        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT password_hash, salt 
                FROM users 
                WHERE username = ?
            """, (username,))
            result = cursor.fetchone()
            if result:
                password_hash, salt = result
                return self._verify_password(password, password_hash, salt)
            return False

    def delete_user(self, username):
        """
        Delete a user from the database.
        
        Args:
            username (str): Username.
        
        Returns:
            str: Success or error message.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE username = ?", (username,))
            if cursor.rowcount > 0:
                conn.commit()
                return f"User '{username}' deleted successfully."
            else:
                return f"Error: User '{username}' not found."

    def list_users(self):
        """
        List all users in the database.
        
        Returns:
            list: A list of usernames.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users")
            return [row[0] for row in cursor.fetchall()]
