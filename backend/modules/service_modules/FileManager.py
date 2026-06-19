"""
FileManager — JSON file read/write helpers for local file-based data persistence.
All data operations go through this module.
"""

import json
import os
import threading

# File lock to prevent concurrent write issues
_file_lock = threading.Lock()

# Base path for data files
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
UPLOADS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")


def ensure_directory(dir_path: str) -> None:
    """Create directory if it doesn't exist."""
    os.makedirs(dir_path, exist_ok=True)


def ensure_file(file_path: str, default=None) -> None:
    """Create a JSON file with default content if it doesn't exist."""
    if default is None:
        default = []
    if not os.path.exists(file_path):
        ensure_directory(os.path.dirname(file_path))
        write_json(file_path, default)


def read_json(file_path: str) -> list | dict:
    """Read and parse a JSON file. Returns empty list if file doesn't exist."""
    if not os.path.exists(file_path):
        return []
    with _file_lock:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)


def write_json(file_path: str, data) -> None:
    """Write data to a JSON file with pretty formatting."""
    ensure_directory(os.path.dirname(file_path))
    with _file_lock:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
