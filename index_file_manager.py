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

    def open_index_file(self, filename):
        """Opens an existing index file."""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' does not exist.")
            return
        try:
            with open(filename, 'rb') as f:
                magic = f.read(8)
                if magic != HEADER_MAGIC:
                    raise FileFormatError(f"Error: File '{filename}' is not a valid index file.")
                root_block = struct.unpack('>Q', f.read(8))[0]
                next_block = struct.unpack('>Q', f.read(8))[0]
                self.header = {'root_block': root_block, 'next_block': next_block}
            self.current_file = filename
            self.btree = BTree(self)
            print(f"Index file '{filename}' opened successfully.")
        except (IOError, FileFormatError) as e:
            logger.error(str(e))
            print(e)

    @require_file_open
    def insert_key_value(self, key, value):
        """Inserts a key/value pair into the B-tree."""
        try:
            if not self.btree:
                self.btree = BTree(self)
            self.btree.insert(key, value)
        except DuplicateKeyError as e:
            logger.error(str(e))
            raise

    @require_file_open
    def search_key(self, key):
        """Searches for a key in the B-tree."""
        if not self.btree:
            self.btree = BTree(self)
        result = self.btree.search(key)
        if result is not None:
            return result
        else:
            raise KeyNotFoundError(f"Error: Key {key} not found in the index.")

    @require_file_open
    def load_from_file(self, filename):
        """Loads key/value pairs from a file into the B-tree."""
        if not os.path.exists(filename):
            print(f"Error: File '{filename}' does not exist.")
            return
        try:
            batch = []
            with open(filename, 'r') as input_file:
                for line in input_file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        key_str, value_str = line.split(',')
                        key = int(key_str.strip())
                        value = int(value_str.strip())
                        if key < 0 or value < 0:
                            print(f"Error: Invalid key/value '{line}'. Skipping.")
                            continue
                        batch.append((key, value))
                    except ValueError:
                        print(f"Error: Invalid line '{line}'. Skipping.")
            # Batch insertion
            for key, value in batch:
                try:
                    self.insert_key_value(key, value)
                except DuplicateKeyError as e:
                    print(e)
            print(f"Loaded key/value pairs from '{filename}'.")
        except IOError as e:
            logger.error(str(e))
            print(f"Error: Could not read from file '{filename}'.")

    @require_file_open
    def print_all(self):
        """Prints all key/value pairs in the B-tree."""
        if not self.btree:
            self.btree = BTree(self)
        all_key_values = []
        self.btree.traverse(all_key_values)
        if all_key_values:
            print("Key/Value pairs in the index:")
            for key, value in all_key_values:
                print(f"Key: {key}, Value: {value}")
        else:
            print("The B-tree is empty.")

    @require_file_open
    def extract_to_file(self, filename):
        """Extracts all key/value pairs to a file."""
        if os.path.exists(filename):
            overwrite = input(f"File '{filename}' already exists. Overwrite? (yes/no): ").strip().lower()
            if overwrite != 'yes':
                print("Aborted extraction.")
                return
        try:
            with open(filename, 'w') as output_file:
                all_key_values = []
                self.btree.traverse(all_key_values)
                for key, value in all_key_values:
                    output_file.write(f"{key},{value}\n")
            print(f"Extracted all key/value pairs to '{filename}'.")
        except IOError as e:
            logger.error(str(e))
            print(f"Error: Could not write to file '{filename}'.")
    def update_header(self):
        """Updates the header information in the index file."""
        try:
            with open(self.current_file, 'r+b') as f:
                f.seek(0)
                f.write(HEADER_MAGIC)
                f.write(struct.pack('>Q', self.header['root_block']))
                f.write(struct.pack('>Q', self.header['next_block']))
                padding_size = BLOCK_SIZE - len(HEADER_MAGIC) - (2 * 8)
                f.write(b'\x00' * padding_size)  # Padding to fill header block
        except IOError as e:
            logger.error(str(e))
            print(f"Error: Could not update header in file '{self.current_file}'.")

class BTreeNode:
    """Represents a node in the B-tree."""

    def __init__(self, index_file_manager, block_id=None, is_new=False):
        self.index_file_manager = index_file_manager
        self.block_id = block_id
        self.parent_block = 0  # Block id of parent, 0 if root
        self.num_keys = 0
        self.keys = []
        self.values = []
        self.children = []
        if is_new:
            self.block_id = self.index_file_manager.header['next_block']
            self.index_file_manager.header['next_block'] += 1
            self._write_node()
            self.index_file_manager.update_header()
        elif block_id is not None:
            self._read_node()

    def _write_node(self):
        """Writes the node to the file at its block position."""
        try:
            with open(self.index_file_manager.current_file, 'r+b') as f:
                f.seek(self.block_id * BLOCK_SIZE)
                data = b''
                data += struct.pack('>Q', self.block_id)
                data += struct.pack('>Q', self.parent_block)
                data += struct.pack('>Q', self.num_keys)
                keys_padded = self.keys + [0] * (19 - len(self.keys))
                values_padded = self.values + [0] * (19 - len(self.values))
                for key in keys_padded:
                    data += struct.pack('>Q', key)
                for value in values_padded:
                    data += struct.pack('>Q', value)
                children_padded = self.children + [0] * (20 - len(self.children))
                for child in children_padded:
                    data += struct.pack('>Q', child)
                data += b'\x00' * (BLOCK_SIZE - len(data))
                f.write(data)
        except IOError as e:
            logger.error(str(e))
            print(f"Error: Could not write node to file '{self.index_file_manager.current_file}'.")

    def _read_node(self):
        """Reads the node from the file at its block position."""
        try:
            with open(self.index_file_manager.current_file, 'rb') as f:
                f.seek(self.block_id * BLOCK_SIZE)
                block_data = f.read(BLOCK_SIZE)
                if len(block_data) < BLOCK_SIZE:
                    print(f"Error: Incomplete block read for block_id {self.block_id}.")
                    return
                self.block_id, self.parent_block, self.num_keys = struct.unpack('>QQQ', block_data[:24])
                offset = 24
                self.keys = []
                for _ in range(19):
                    key = struct.unpack('>Q', block_data[offset:offset+8])[0]
                    self.keys.append(key)
                    offset +=8
                self.values = []
                for _ in range(19):
                    value = struct.unpack('>Q', block_data[offset:offset+8])[0]
                    self.values.append(value)
                    offset +=8
                self.children = []
                for _ in range(20):
                    child = struct.unpack('>Q', block_data[offset:offset+8])[0]
                    self.children.append(child)
                    offset +=8
                self.keys = self.keys[:self.num_keys]
                self.values = self.values[:self.num_keys]
                self.children = self.children[:self.num_keys+1] if any(self.children) else []
        except IOError as e:
            logger.error(str(e))
            print(f"Error: Could not read node from file '{self.index_file_manager.current_file}'.")

    def is_leaf(self):
        """Checks if the node is a leaf node."""
        return len(self.children) == 0

    def insert_non_full(self, key, value):
        """Inserts a key/value pair into a node that is not full."""
        i = self.num_keys -1
        if self.is_leaf():
            self.keys.append(0)
            self.values.append(0)
            while i >=0 and key < self.keys[i]:
                self.keys[i+1] = self.keys[i]
                self.values[i+1] = self.values[i]
                i -=1
            if i >=0 and key == self.keys[i]:
                raise DuplicateKeyError(f"Error: Key {key} already exists in the index.")
            self.keys[i+1] = key
            self.values[i+1] = value
            self.num_keys +=1
            self._write_node()
            return True
        else:
            while i >=0 and key < self.keys[i]:
                i -=1
            i +=1
            child_node = BTreeNode(self.index_file_manager, self.children[i])
            if child_node.num_keys == 2*MIN_DEGREE -1:
                self.split_child(i, child_node)
                if key > self.keys[i]:
                    i +=1
                elif key == self.keys[i]:
                    raise DuplicateKeyError(f"Error: Key {key} already exists in the index.")
            child_node = BTreeNode(self.index_file_manager, self.children[i])
            return child_node.insert_non_full(key, value)

    def split_child(self, i, y):
        """Splits a full child node."""
        z = BTreeNode(self.index_file_manager, is_new=True)
        z.parent_block = self.block_id
        t = MIN_DEGREE
        z.num_keys = t -1
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        if not y.is_leaf():
            z.children = y.children[t:]
        y.keys = y.keys[:t-1]
        y.values = y.values[:t-1]
        y.children = y.children[:t] if not y.is_leaf() else []
        y.num_keys = t -1
        y._write_node()
        z._write_node()
        self.keys.insert(i, y.keys.pop())
        self.values.insert(i, y.values.pop())
        self.children.insert(i+1, z.block_id)
        self.num_keys +=1
        self._write_node()
        y.parent_block = self.block_id
        y._write_node()
        z.parent_block = self.block_id
        z._write_node()

    def search(self, key):
        """Searches for a key in the subtree rooted at this node."""
        i = 0
        while i < self.num_keys and key > self.keys[i]:
            i +=1
        if i < self.num_keys and key == self.keys[i]:
            return self.values[i]
        elif self.is_leaf():
            return None
        else:
            child_node = BTreeNode(self.index_file_manager, self.children[i])
            return child_node.search(key)
    
    def traverse(self, result_list):
        """Performs an in-order traversal of the subtree rooted at this node."""
        for i in range(self.num_keys):
            if not self.is_leaf():
                child_node = BTreeNode(self.index_file_manager, self.children[i])
                child_node.traverse(result_list)
            result_list.append((self.keys[i], self.values[i]))
        if not self.is_leaf():
            child_node = BTreeNode(self.index_file_manager, self.children[self.num_keys])
            child_node.traverse(result_list)

class BTree:
    """Represents the B-tree structure."""

    def __init__(self, index_file_manager):
        self.index_file_manager = index_file_manager
        self.root = None
        if self.index_file_manager.header['root_block'] == 0:
            pass
        else:
            self.root = BTreeNode(self.index_file_manager, self.index_file_manager.header['root_block'])

    def insert(self, key, value):
        """Inserts a key/value pair into the B-tree."""
        if self.root is None:
            self.root = BTreeNode(self.index_file_manager, is_new=True)
            self.root.keys.append(key)
            self.root.values.append(value)
            self.root.num_keys = 1
            self.index_file_manager.header['root_block'] = self.root.block_id
            self.root._write_node()
            self.index_file_manager.update_header()
        else:
            if self.root.num_keys == 2*MIN_DEGREE -1:
                s = BTreeNode(self.index_file_manager, is_new=True)
                s.children.append(self.root.block_id)
                s.num_keys = 0
                self.root.parent_block = s.block_id
                self.root._write_node()
                s.split_child(0, self.root)
                self.root = s
                self.index_file_manager.header['root_block'] = self.root.block_id
                self.index_file_manager.update_header()
                self.root.insert_non_full(key, value)
            else:
                self.root.insert_non_full(key, value)
    
    def search(self, key):
        """Searches for a key in the B-tree."""
        if self.root is None:
            return None
        else:
            return self.root.search(key)

    def traverse(self, result_list):
        """Traverses the B-tree and collects key/value pairs."""
        if self.root:
            self.root.traverse(result_list)

def main():
    """Main function to start the program."""
    index_file_manager = IndexFileManager()
    command_handler = CommandHandler(index_file_manager)
    command_handler.start()

if __name__ == "__main__":
    main()