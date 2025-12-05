"""File handling utilities for safe reading and writing."""

import re
import sys


class FileHandler:
    """Handles safe file operations preserving escape sequences."""
    
    @staticmethod
    def sanitize_filename(title):
        """Clean a title to make it a valid filename."""
        title = re.sub(r'[\n\t]+', ' ', title).strip()
        safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
        safe_title = re.sub(r'[ .]+', '_', safe_title)
        return safe_title[:100].strip('_')
    
    @staticmethod
    def sanitize_dirname(name):
        """Clean a category name to make it a valid directory name."""
        name = re.sub(r'[\n\t]+', ' ', name).strip()
        safe_name = re.sub(r'[<>:"/\\|?*]', '', name)
        safe_name = re.sub(r'[ ]+', '_', safe_name)
        return safe_name.strip('_')
    
    @staticmethod
    def safe_read_preserving_escapes(filepath):
        """Read a file preserving all escape sequences."""
        try:
            with open(filepath, 'r', encoding='utf-8', newline='') as f:
                return f.read()
        except Exception as e:
            print(f"  Error reading {filepath}: {e}", file=sys.stderr)
            return None
    
    @staticmethod
    def safe_write_preserving_escapes(filepath, content):
        """Write content preserving escape sequences."""
        try:
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"  Error writing {filepath}: {e}", file=sys.stderr)
            return False
