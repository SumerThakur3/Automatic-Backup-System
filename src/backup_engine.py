import os
import shutil
from src.logger import log_info, log_error
from src.utils import calculate_file_hash, ensure_directory

class BackupEngine:

    def __init__(self, backup_folder):
        self.backup_folder = backup_folder
        self.backed_up_files = 0

    def backup_file(self, source_path, source_root):

        try:

            filename = os.path.basename(source_path)

            if not os.path.exists(source_path):
                return None

            relative_path = os.path.relpath(
                source_path,
                source_root
            )

            destination_path = os.path.join(
                self.backup_folder,
                relative_path
            )

            destination_dir = os.path.dirname(
                destination_path
            )

            ensure_directory(destination_dir)

            # Duplicate detection
            if os.path.exists(destination_path):

                source_hash = calculate_file_hash(source_path)
                dest_hash = calculate_file_hash(destination_path)

                if source_hash == dest_hash:
                    return "DUPLICATE"

            shutil.copy2(source_path, destination_path)

            self.backed_up_files += 1

            return f"{filename} backed up"

        except PermissionError:
            return "Permission denied"

        except Exception as e:
            return str(e)