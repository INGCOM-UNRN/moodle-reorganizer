"""
Question Bank Backup and Reorganizer

A tool for backing up and reorganizing question banks in GIFT or Moodle XML format.
Allows exporting questions from a monolithic file to a directory structure based on categories,
and collecting questions from a directory structure to regenerate a monolithic file.
"""

__version__ = "1.0.0"

from .reorganizer import QuestionBackupReorganizer
from .cli import main

__all__ = ["QuestionBackupReorganizer", "main"]
