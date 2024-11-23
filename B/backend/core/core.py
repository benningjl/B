import logging
import sqlite3
import os
import sys
from network_manager import NetworkManager
from security_manager import SecurityManager
from encryption_manager import EncryptionManager
from user_manager import UserManager

class Core:
    def __init__(self, host="127.0.0.1", port=8080, db_path="F:/B/backend/db/ghnet.db"):
        """
        Initializes the core system for the backend.
        :param host: The host IP for the network manager.
        :param port: The port number for the network manager.
        :param db_path: The path to the SQLite database.
        """
        self.host = host
        self.port = port
        self.db_path = db_path
        
        # Initialize logging
        self.logger = self.setup_logger()
        
        # Initialize the core services
        self.db_connection = None
        self.network_manager = None
        self.security_manager = None
        self.encryption_manager = None
        self.user_manager = None

    def setup_logger(self):
        """Sets up the logging for the core system."""
        logger = logging.getLogger("CoreLogger")
        logger.setLevel(logging.INFO)
        
        # Ensure log directory exists
        log_dir = "F:/B/logs"
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, "core.log")
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        return logger

    def initialize_database(self):
        """Initialize database connection."""
        try:
            self.db_connection = sqlite3.connect(self.db_path)
            self.logger.info(f"Database connected at {self.db_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Database connection error: {e}")
            sys.exit(1)

    def initialize_services(self):
        """Initialize all required backend services."""
        self.logger.info("Initializing backend services...")
        
        # Initialize network manager
        self.network_manager = NetworkManager(self.host, self.port)
        self.network_manager.start_server()
        
        # Initialize security manager
        self.security_manager = SecurityManager(self.db_connection)
        
        # Initialize encryption manager
        self.encryption_manager = EncryptionManager(self.db_connection)
        
        # Initialize user manager
        self.user_manager = UserManager(self.db_connection)
        
        self.logger.info("All services initialized successfully.")

    def start(self):
        """Start the core system."""
        self.logger.info("Starting Core System...")
        
        # Initialize database connection
        self.initialize_database()

        # Initialize services
        self.initialize_services()
        
        self.logger.info("Core system started successfully.")

    def stop(self):
        """Stop the core system and close connections."""
        self.logger.info("Stopping Core System...")
        
        # Stop all services
        if self.network_manager:
            self.network_manager.stop_server()
        
        # Close the database connection
        if self.db_connection:
            self.db_connection.close()
        
        self.logger.info("Core system stopped successfully.")
    
    def restart(self):
        """Restart the core system."""
        self.logger.info("Restarting Core System...")
        self.stop()
        self.start()

    def handle_error(self, error_message):
        """Handles errors by logging and sending appropriate responses."""
        self.logger.error(f"Error occurred: {error_message}")
        # You can extend this method to handle specific actions like sending alerts, etc.

if __name__ == "__main__":
    # Initialize the core system with default settings
    core_system = Core()
    
    try:
        core_system.start()
        # The system runs indefinitely, waiting for service requests
        while True:
            pass
    except KeyboardInterrupt:
        core_system.stop()
    except Exception as e:
        core_system.handle_error(str(e))
