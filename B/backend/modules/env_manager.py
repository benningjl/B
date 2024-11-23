import os
from dotenv import load_dotenv

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
        self.env_variables = {}

    def load_env(self):
        """
        Load environment variables from the .env file.

        Returns:
            bool: True if environment variables were successfully loaded, False otherwise.
        """
        if os.path.exists(self.env_file_path):
            # Load environment variables from the file
            load_dotenv(self.env_file_path)
            
            # Populate the dictionary with environment variables
            for key, value in os.environ.items():
                self.env_variables[key] = value
            
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
        return self.env_variables.get(key)

    def set_env_var(self, key, value):
        """
        Set an environment variable in the current session.

        Args:
            key (str): The key of the environment variable.
            value (str): The value of the environment variable.
        """
        os.environ[key] = value
        self.env_variables[key] = value  # Also update the internal dictionary

    def is_env_loaded(self):
        """
        Checks if the environment has been loaded successfully.

        Returns:
            bool: True if environment variables have been loaded, False otherwise.
        """
        return bool(self.env_variables)


# Example usage
if __name__ == "__main__":
    env_manager = EnvManager("F:\\B\\backend\\.env")
    
    if env_manager.load_env():
        print("Environment variables loaded successfully.")
        # Example: Fetching a specific environment variable
        sample_env_var = env_manager.get_env_var('SAMPLE_ENV_VAR')
        print(f"Sample ENV_VAR: {sample_env_var}")
    else:
        print("Failed to load environment variables.")
