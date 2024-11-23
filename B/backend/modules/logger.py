import os
import logging
from logging.handlers import RotatingFileHandler


class Logger:
    """
    A class to manage logging for the application.
    """

    def __init__(self, log_file_path="F:\\B\\backend\\logs\\app.log", max_log_size=5 * 1024 * 1024, backup_count=3):
        """
        Initialize the Logger instance.

        Args:
            log_file_path (str): Path to the log file.
            max_log_size (int): Maximum size of a single log file in bytes.
            backup_count (int): Number of backup files to keep.
        """
        self.log_file_path = os.path.abspath(log_file_path)
        self.max_log_size = max_log_size
        self.backup_count = backup_count
        self.logger = logging.getLogger("ProjectBLogger")
        self.logger.setLevel(logging.DEBUG)
        self._setup_handlers()

    def _setup_handlers(self):
        """
        Set up file and console handlers for the logger.
        """
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(self.log_file_path)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        # File handler with log rotation
        file_handler = RotatingFileHandler(
            self.log_file_path,
            maxBytes=self.max_log_size,
            backupCount=self.backup_count
        )
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)

        # Adding handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log(self, level, message):
        """
        Log a message with the specified level.

        Args:
            level (str): Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
            message (str): Message to log.
        """
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)
        else:
            self.logger.info(f"Unknown level: {message}")

    def debug(self, message):
        """Log a debug message."""
        self.log("DEBUG", message)

    def info(self, message):
        """Log an info message."""
        self.log("INFO", message)

    def warning(self, message):
        """Log a warning message."""
        self.log("WARNING", message)

    def error(self, message):
        """Log an error message."""
        self.log("ERROR", message)

    def critical(self, message):
        """Log a critical message."""
        self.log("CRITICAL", message)


# Example usage
if __name__ == "__main__":
    log_manager = Logger()
    log_manager.info("Application started.")
    log_manager.debug("Debugging message.")
    log_manager.warning("Warning message.")
    log_manager.error("Error message.")
    log_manager.critical("Critical error!")
