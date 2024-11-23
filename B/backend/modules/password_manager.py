import bcrypt

class PasswordManager:
    def __init__(self):
        """Initialize the PasswordManager."""
        pass

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password (str): The plain-text password to hash.
        
        Returns:
            str: The hashed password.
        """
        # Generate a salt with a cost factor of 12 (common default)
        salt = bcrypt.gensalt(rounds=12)
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def check_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Check if the plain-text password matches the hashed password.
        
        Args:
            plain_password (str): The plain-text password to check.
            hashed_password (str): The stored hashed password.
        
        Returns:
            bool: True if passwords match, False otherwise.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

