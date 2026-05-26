import hashlib
import os

def calculate_file_hash(filepath):
    """
    Calculate MD5 hash of file.
    Used for duplicate detection.
    """
    hash_md5 = hashlib.md5()

    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    except Exception:
        return None


def ensure_directory(path):
    """
    Create directory if it doesn't exist.
    """
    os.makedirs(path, exist_ok=True)