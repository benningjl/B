import psycopg2
from psycopg2 import sql
import hashlib
import time

class SessionManager:
    def __init__(self, db_config):
        self.db_config = db_config

    def _get_connection(self):
        """Establish a connection to the database."""
        connection = psycopg2.connect(**self.db_config)
        return connection

    def create_session(self, username, expiration_duration=1800):
        """Create a session for a user and return the session token."""
        session_token = self._generate_session_token()
        expiration_time = int(time.time()) + expiration_duration  # Default expiration time is 30 minutes

        try:
            query = sql.SQL("""
                INSERT INTO sessions (session_token, username, expiration_time)
                VALUES (%s, %s, %s)
            """)
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (session_token, username, expiration_time))
                    conn.commit()
                    print(f"Session created successfully for {username}.")
                    return session_token
        except Exception as e:
            print(f"An error occurred while creating the session: {e}")
            return None

    def validate_session(self, session_token):
        """Validate the session by checking its existence and expiration."""
        try:
            query = sql.SQL("""
                SELECT username, expiration_time FROM sessions WHERE session_token = %s
            """)
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (session_token,))
                    result = cursor.fetchone()

                    if result:
                        username, expiration_time = result
                        # Check if the session has expired
                        if int(time.time()) <= expiration_time:
                            return username
                        else:
                            print("Session expired.")
                            self.logout(session_token)  # Optional: Automatically logout after expiration
                            return None
                    else:
                        print("Session not found.")
                        return None
        except Exception as e:
            print(f"An error occurred while validating the session: {e}")
            return None

    def logout(self, session_token):
        """Logout the user by deleting their session."""
        try:
            query = sql.SQL("""
                DELETE FROM sessions WHERE session_token = %s
            """)
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (session_token,))
                    conn.commit()
                    print("Session deleted successfully.")
        except Exception as e:
            print(f"An error occurred while logging out: {e}")

    def get_user_data(self, session_token):
        """Fetch user data only if the session is valid."""
        username = self.validate_session(session_token)
        if username:
            try:
                query = sql.SQL("""
                    SELECT username, email FROM users WHERE username = %s
                """)
                with self._get_connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(query, (username,))
                        result = cursor.fetchone()
                        if result:
                            print(f"User Data: {result}")
                            return result
                        else:
                            print("User not found.")
                            return None
            except Exception as e:
                print(f"An error occurred while fetching user data: {e}")
                return None
        else:
            print("Invalid session.")
            return None

    def _generate_session_token(self):
        """Generate a random session token."""
        # For simplicity, using a hash of the current time to generate a session token
        return hashlib.sha256(str(time.time()).encode('utf-8')).hexdigest()
