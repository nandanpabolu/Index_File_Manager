# DevLog

## November 30th 9:59 am

**Thoughts:**

Starting the B-Tree Index Manager project. Planning to create an interactive program that manages index files containing a B-tree.

**Plan:**

    - Set up the project structure.
    - Decide on the programming language (Python).
    - Create the initial files.
    - plan out classes, functions and steructure of code on whiteboard

**Actions:**

    - Created the Git repository.
    - Created the `devlog.md` file.
    - started coding, implementing basic functions
    - implemented error classes- DuplicateKeyError, FileFormatError, KeyNotFoundEroor, InvalidCommandError

## November 30th 6:39 pm

**Thoughts:**

I recognized that several methods in the IndexFileManager class should only be executed when an index file is open. Without an open file, these methods shouldn’t proceed, and adding repetitive checks in each method isn’t efficient or clean. To address this, I decided to implement a decorator named require_file_open that ensures an index file is open before the method executes.

Additionally, I needed a way to handle user inputs and commands systematically. To achieve this, I planned to create a CommandHandler class responsible for starting the command loop, parsing user commands, and dispatching them to the appropriate handlers. This class would also need to handle exceptions gracefully, such as KeyboardInterrupt and EOFError, to allow users to exit the program cleanly.

**Plan:**

	•	Implement the require_file_open Decorator:
	•	Create a decorator that checks if self.current_file is set before executing the decorated method.
	•	If no file is open, print an error message and prevent the method from running.
	•	Develop the CommandHandler Class:
	•	Initialize the class with a reference to the IndexFileManager.
	•	Implement the start method to begin the command loop and prompt the user for input.
	•	Implement the handle_command method to parse user input into commands and arguments.
	•	Handle known commands and raise an error for invalid ones.
	•	Gracefully handle exceptions like KeyboardInterrupt and EOFError.

**Actions Taken:**

	•	Created the require_file_open decorator to enforce that certain methods only run when an index file is open.
	•	Developed the CommandHandler class with methods to start the command loop and handle user commands.
	•	Added exception handling in the command loop to catch KeyboardInterrupt and EOFError, allowing the program to exit cleanly when the user presses Ctrl+C or sends an EOF signal.
	•	Ensured that the handle_command method parses user input correctly and dispatches commands to the appropriate handler methods.


## November 30th 10:15 pm

**Thoughts:**

After setting up the basic command loop and the CommandHandler class, I realized that I needed to implement the actual handling of each command. This involves mapping user commands to specific methods that execute the desired functionality. Additionally, I needed to start implementing the core functionalities in the IndexFileManager class, beginning with creating and opening index files.

**Plan:**

	•	Implement Command Handlers:
	•	Define individual handler methods for each supported command in the CommandHandler class.
	•	Map user commands to these handler methods using a dictionary.
	•	Ensure proper input validation and error handling in each handler.
	•	Implement Index File Creation:
	•	In the IndexFileManager, implement the create_and_open_index_file method to handle index file creation.
	•	Write a header to the new index file, including a magic number and initial values.
	•	Implement error handling for file operations.
	•	Connect Command Handlers to Index File Operations:
	•	In the command handlers, call the appropriate methods in IndexFileManager to perform the actual operations.
	•	Provide user feedback by printing success or error messages.

**Actions Taken:**

	1.	Mapped Commands to Handler Methods:
	•	Created a command_methods dictionary in the CommandHandler class that maps command strings to their corresponding handler methods.
	•	Implemented logic to look up the command and execute the associated method, passing in any arguments.
	2.	Implemented Command Handler Methods:
	•	For each command (create, open, insert, search, load, print, extract, quit, help), I defined a _handle_<command> method.
	•	Each method performs input validation, such as checking the number of arguments and ensuring inputs are of the correct type.
	•	Added error handling for exceptions like ValueError, DuplicateKeyError, and KeyNotFoundError.
	•	Provided informative messages to the user for both successful operations and errors.
	3.	Implemented Index File Creation in IndexFileManager:
	•	Created the create_and_open_index_file method to handle the creation of a new index file.
	•	Added a check to see if the file already exists and, if so, prompt the user for confirmation before overwriting.
	•	Implemented the _write_header_to_file method to write the necessary header information to the new index file.
	•	Wrote a magic number (HEADER_MAGIC) to identify valid index files.
	•	Initialized root_block and next_block IDs.
	•	Added padding to fill up the header block to the specified block size.
	4.	Connected Command Handlers to Index File Operations:
	•	In the _handle_create and _handle_open methods, called the corresponding methods in IndexFileManager.
	•	Ensured that user feedback is provided by printing appropriate messages based on the success or failure of the operations.
	5.	Ensured Proper Error Handling and Input Validation:
	•	In the command handlers, checked that the correct number of arguments is provided.
	•	Converted input strings to integers where necessary and validated that they are non-negative.
	•	Caught and handled specific exceptions, providing clear error messages to the user.