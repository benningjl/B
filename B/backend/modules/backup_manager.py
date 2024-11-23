import shutil
import os
from datetime import datetime

class BackupManager:
    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def backup_file(self, file_path):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"{file_path} does not exist.")
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.backup_dir, f"{os.path.basename(file_path)}_{timestamp}")
            shutil.copy(file_path, backup_path)
            print(f"Backup created at: {backup_path}")
        except Exception as e:
            print(f"Backup failed: {e}")
