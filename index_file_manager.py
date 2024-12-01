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

# I wrote a decorator to ensure that certain methods are only called when an index file is open.
def require_file_open(method):
    """Decorator to ensure a file is open before executing certain methods."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_file:
            print("Error: No index file is open.")
            return
        return method(self, *args, **kwargs)
    return wrapper

class CommandHandler:
    """Handles user commands and input parsing."""

    def __init__(self, index_file_manager):
        # I initialized the command handler with a reference to the index file manager.
        self.index_file_manager = index_file_manager

    def start(self):
        """Starts the command loop."""
        print("Welcome to the B-Tree Index Manager. Type 'help' for a list of commands.")
        try:
            while True:
                user_input = input("Enter command: ").strip()
                if not user_input:
                    continue
                try:
                    self.handle_command(user_input)
                except InvalidCommandError as e:
                    print(e)
                except KeyboardInterrupt:
                    print("\nExiting program.")
                    sys.exit(0)
        except EOFError:
            print("\nExiting program.")
            sys.exit(0)

    def handle_command(self, user_input):
        """Parses and dispatches the user command."""
        # I split the user input into command and arguments.
        parts = user_input.strip().split()
        command = parts[0].lower()
        args = parts[1:]