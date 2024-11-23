import logging

class ActivityLogger:
    def __init__(self, log_file='activity.log'):
        self.logger = logging.getLogger('ActivityLogger')
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_action(self, user, action, status):
        self.logger.info(f"User: {user}, Action: {action}, Status: {status}")
