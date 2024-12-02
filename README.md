# B-Tree Index Manager

## Overview

The **B-Tree Index Manager** is a command-line application that allows users to create and manage a B-Tree index file. It supports operations such as creating a new index file, opening an existing index file, inserting key/value pairs, searching for keys, loading data from a file, printing all entries, and extracting data to a file.

## Files and Their Roles

- **`main.py`**: The main Python script containing all the code for the B-Tree Index Manager. It includes the following classes and components:
  - `IndexFileManager`: Manages index file operations such as creating, opening, inserting, searching, loading, printing, and extracting.
  - `CommandHandler`: Handles user commands and input parsing.
  - `BTree`: Represents the B-Tree structure and manages insertion and search operations.
  - `BTreeNode`: Represents a node in the B-Tree and handles node-specific operations.
  - **Custom Exceptions**: Defines custom exceptions for error handling.
  - **Decorators**: Includes a decorator to ensure certain methods are only called when an index file is open.

## How to Run the Program

### Prerequisites

- **Python 3.x** installed on your system.
- Ensure that all necessary files are in the same directory.

### Running the Program

1. **Open a Command-Line Terminal**:

   - On **Windows**: Use Command Prompt or PowerShell.
   - On **macOS/Linux**: Use Terminal.

2. **Navigate to the Program Directory**:

   ```bash
   cd /path/to/directory

3. **Run the program**:
    python3 main.py

4. **Using the Program**
	•	Upon starting, the program will display a welcome message:
    Welcome to the B-Tree Index Manager. Type 'help' for a list of commands.

	•	List of Available Commands:
	•	create <filename>: Create a new index file with the specified filename and open it.
	•	open <filename>: Open an existing index file.
	•	insert <key> <value>: Insert a key/value pair into the index.
	•	key: An unsigned integer representing the key.
	•	value: An unsigned integer representing the value.
	•	search <key>: Search for a key in the index and display its value if found.
	•	load <filename>: Load key/value pairs from a file.
	•	The file should contain one key/value pair per line, separated by a comma (e.g., 123,456).
	•	print: Print all key/value pairs in the index in sorted order.
	•	extract <filename>: Extract all key/value pairs to a file.
	•	quit: Exit the program.
	•	help: Display the help message with a list of available commands.

5. **Notes to the TA:21 qq`**

	•	Data File Format for Loading:
	•	When using the load command, the input file should be formatted with one key/value pair per line.
	•	Each line should be in the format: <key>,<value> (e.g., 123,456).
	•	Both key and value must be unsigned integers.
	•	Index File Structure:
	•	The index file is a binary file with a specific format.
	•	It starts with a header containing a magic number (b'4337PRJ3'), the root block ID, and the next block ID.
	•	Each node in the B-Tree is stored in a fixed-size block of 512 bytes.
	•	B-Tree Parameters:
	•	The B-Tree uses a minimum degree (MIN_DEGREE) of 10.
	•	This means each node can have a maximum of 2 * MIN_DEGREE - 1 keys.
	•	Error Handling:
	•	The program includes error handling for:
	•	Invalid commands.
	•	File I/O errors.
	•	Duplicate keys during insertion.
	•	Searching for non-existent keys.
	•	Incorrect file formats.
	•	Logging:
	•	The program uses Python’s logging module to log errors.
	•	By default, logging is set to the ERROR level.
	•	Logs are printed to the console for immediate feedback.
	•	Testing:
	•	The program has been tested with various inputs and edge cases.
	•	If you encounter any issues or unexpected behavior, please let me know.
	•	Program Termination:
	•	Use the quit command or press Ctrl+C to exit the program gracefully.
	•	The program handles KeyboardInterrupt and EOFError exceptions to ensure a clean exit.
	•	Assumptions:
	•	Keys and values are assumed to be unsigned integers.
	•	The maximum key and value size is determined by the system’s maximum integer size in Python.

6. **Additional Information:**

	•	Extensibility:
	•	The program is designed with modularity in mind.
	•	Additional commands and functionalities can be added by extending the CommandHandler and associated classes.
	•	Code Structure:
	•	The code follows object-oriented programming principles.
	•	Classes are used to encapsulate functionality and maintain state.
	•	Decorator Usage:
	•	The @require_file_open decorator ensures that certain methods in IndexFileManager are only executed when an index file is open.
	•	This prevents unintended operations and improves error handling.