import os
import struct
import functools
import sys
import logging

BLOCK_SIZE = 512
HEADER_MAGIC = b'4337PRJ3'
MIN_DEGREE = 10  # Minimal degree t of B-tree

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Custom Exceptions
class IndexFileError(Exception):
    """Base class for index file exceptions."""
    pass

class DuplicateKeyError(IndexFileError):
    """Exception raised when a duplicate key is inserted."""
    pass

class FileFormatError(IndexFileError):
    """Exception raised when the file format is incorrect."""
    pass

class KeyNotFoundError(IndexFileError):
    """Exception raised when a key is not found during search."""
    pass

class InvalidCommandError(Exception):
    """Exception raised for invalid commands."""
    pass