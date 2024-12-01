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
        command_methods = {
            'create': self._handle_create,
            'open': self._handle_open,
            'insert': self._handle_insert,
            'search': self._handle_search,
            'load': self._handle_load,
            'print': self._handle_print,
            'extract': self._handle_extract,
            'quit': self._handle_quit,
            'help': self._handle_help
        }

        if command in command_methods:
            command_methods[command](args)
        else:
            raise InvalidCommandError("Invalid command. Type 'help' for a list of commands.")

    def _handle_create(self, args):
        if len(args) != 1:
            print("Usage: create <filename>")
            return
        filename = args[0]
        self.index_file_manager.create_and_open_index_file(filename)

    def _handle_open(self, args):
        if len(args) != 1:
            print("Usage: open <filename>")
            return
        filename = args[0]
        self.index_file_manager.open_index_file(filename)

    def _handle_insert(self, args):
        if len(args) != 2:
            print("Usage: insert <key> <value>")
            return
        try:
            key = int(args[0])
            value = int(args[1])
            if key < 0 or value < 0:
                print("Error: Keys and values must be unsigned integers.")
                return
            self.index_file_manager.insert_key_value(key, value)
            print(f"Successfully inserted key {key}.")
        except ValueError:
            print("Error: Keys and values must be unsigned integers.")
        except DuplicateKeyError as e:
            print(e)

    def _handle_search(self, args):
        if len(args) != 1:
            print("Usage: search <key>")
            return
        try:
            key = int(args[0])
            if key < 0:
                print("Error: Keys must be unsigned integers.")
                return
            value = self.index_file_manager.search_key(key)
            print(f"Found key {key} with value {value}.")
        except ValueError:
            print("Error: Keys must be unsigned integers.")
        except KeyNotFoundError as e:
            print(e)

    def _handle_load(self, args):
        if len(args) != 1:
            print("Usage: load <filename>")
            return
        filename = args[0]
        self.index_file_manager.load_from_file(filename)

    def _handle_print(self, args):
        self.index_file_manager.print_all()

    def _handle_extract(self, args):
        if len(args) != 1:
            print("Usage: extract <filename>")
            return
        filename = args[0]
        self.index_file_manager.extract_to_file(filename)

    def _handle_quit(self, args):
        confirm = input("Are you sure you want to quit? (yes/no): ").strip().lower()
        if confirm == 'yes':
            print("Exiting program.")
            sys.exit(0)

    def _handle_help(self, args):
        help_text = """
Available commands:
  create <filename>      Create a new index file.
  open <filename>        Open an existing index file.
  insert <key> <value>   Insert a key/value pair into the index.
  search <key>           Search for a key in the index.
  load <filename>        Load key/value pairs from a file.
  print                  Print all key/value pairs in the index.
  extract <filename>     Extract all key/value pairs to a file.
  quit                   Exit the program.
  help                   Show this help message.
"""
        print(help_text)

class IndexFileManager:
    """Manages index file operations."""

    def __init__(self):
        self.current_file = None
        self.header = None  # {'root_block': int, 'next_block': int}
        self.btree = None  # Instance of BTree

    def create_and_open_index_file(self, filename):
        """Creates and opens a new index file."""
        if os.path.exists(filename):
            overwrite = input(f"File '{filename}' already exists. Overwrite? (yes/no): ").strip().lower()
            if overwrite != 'yes':
                print("Aborted file creation.")
                return
        try:
            self._write_header_to_file(filename)
            self.open_index_file(filename)
            print(f"Index file '{filename}' created and opened successfully.")
        except IndexFileError as e:
            print(e)

    def _write_header_to_file(self, filename):
        """Writes the header to a new index file."""
        try:
            with open(filename, 'wb') as f:
                f.write(HEADER_MAGIC)
                f.write(struct.pack('>Q', 0))  # Root block ID (initially zero)
                f.write(struct.pack('>Q', 1))  # Next block ID to be added (starts at 1)
                padding_size = BLOCK_SIZE - len(HEADER_MAGIC) - (2 * 8)
                f.write(b'\x00' * padding_size)  # Padding to fill header block
        except IOError as e:
            logger.error(f"Could not write header to file '{filename}'. {str(e)}")
            raise IndexFileError(f"Error: Could not create index file '{filename}'.")
        
        #Stopped here, need some rest and will begin tomorrow!