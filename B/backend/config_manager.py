import os
import json

class ConfigManager:
    """
    A class to manage application configuration settings.
    """
    DEFAULT_CONFIG = {
        "logging": {
            "log_file_path": "F:\\B\\backend\\logs\\app.log",
            "max_log_size": 5 * 1024 * 1024,  # 5 MB
            "backup_count": 3
        },
        "server": {
            "host": "127.0.0.1",
            "port": 8080
        },
        "database": {
            "db_name": "app_database",
            "db_user": "admin",
            "db_password": "password",
            "db_host": "localhost",
            "db_port": 5432
        }
    }

    def __init__(self, config_file="F:\\B\\backend\\config\\config.json"):
        """
        Initialize the ConfigManager instance.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config_file = config_file
        self.config = {}
        self._load_config()

    def _load_config(self):
        """
        Load configuration from the file or create a default one if it doesn't exist.
        """
        if not os.path.exists(self.config_file):
            self._create_default_config()
        else:
            with open(self.config_file, "r") as file:
                self.config = json.load(file)

    def _create_default_config(self):
        """
        Create a default configuration file if none exists.
        """
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, "w") as file:
            json.dump(self.DEFAULT_CONFIG, file, indent=4)
        self.config = self.DEFAULT_CONFIG

    def get(self, key, default=None):
        """
        Retrieve a configuration value.

        Args:
            key (str): Dot-separated key (e.g., 'server.host').
            default: Default value if the key does not exist.

        Returns:
            The value associated with the key or the default value.
        """
        keys = key.split(".")
        value = self.config
        for k in keys:
            if k in value:
                value = value[k]
            else:
                return default
        return value

    def set(self, key, value):
        """
        Set a configuration value.

        Args:
            key (str): Dot-separated key (e.g., 'server.port').
            value: Value to set.
        """
        keys = key.split(".")
        config_section = self.config
        for k in keys[:-1]:
            if k not in config_section:
                config_section[k] = {}
            config_section = config_section[k]
        config_section[keys[-1]] = value
        self._save_config()

    def _save_config(self):
        """
        Save the configuration to the file.
        """
        with open(self.config_file, "w") as file:
            json.dump(self.config, file, indent=4)

# Example usage
if __name__ == "__main__":
    config_manager = ConfigManager()
    print("Server Host:", config_manager.get("server.host"))
    print("Database Name:", config_manager.get("database.db_name"))
    
    config_manager.set("server.port", 9090)
    print("Updated Server Port:", config_manager.get("server.port"))
