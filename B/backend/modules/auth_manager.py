from session_manager import SessionManager
from password_manager import PasswordManager
import psycopg2
from psycopg2 import sql
from datetime import datetime

class AuthManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.session_manager = SessionManager(db_config)  # Initialize SessionManager

    def _get_connection(self):
        """Establish a connection to the database."""
        connection = psycopg2.connect(**self.db_config)
        return connection

    def register_user(self, username, email, password):
        """Register a new user."""
        try:
            hashed_password = PasswordManager.hash_password(password)
            query = sql.SQL("""
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
            """)
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (username, email, hashed_password))
                    conn.commit()
                    print("User registered successfully.")
        except Exception as e:
            print(f"An error occurred while registering user: {e}")

    def login_user(self, username, password):
        """Authenticate user and create a session."""
        try:
            query = sql.SQL("""
                SELECT password FROM users WHERE username = %s
            """)
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (username,))
                    result = cursor.fetchone()

                    if result:
                        stored_password = result[0]
                        if PasswordManager.verify_password(password, stored_password):
                            # Create a session after successful login
                            session_token = self.session_manager.create_session(username)
                            print("User logged in successfully.")
                            return session_token
                        else:
                            print("Invalid password.")
                            return None
                    else:
                        print("User not found.")
                        return None
        except Exception as e:
            print(f"An error occurred while logging in: {e}")
            return None

    def logout_user(self, session_token):
        """Logout the user by deleting their session."""
        try:
            self.session_manager.logout(session_token)
            print("User logged out successfully.")
        except Exception as e:
            print(f"An error occurred while logging out: {e}")
