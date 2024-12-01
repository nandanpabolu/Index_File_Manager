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
