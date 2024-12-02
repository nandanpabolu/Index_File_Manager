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

## December 1st 12:53 pm
 **Thoughts:**

    After setting up the command handlers and basic index file creation, I needed to implement the core functionalities of the IndexFileManager class that interact with the B-tree. This includes opening existing index files, inserting key/value pairs, searching for keys, loading data from files, printing all entries, and extracting data to files. These methods are crucial for the program’s operation and require careful error handling and validation.

**Plan:**

        •	Implement the open_index_file Method:
        •	Open an existing index file and validate its format.
        •	Read the header information to initialize the B-tree.
        •	Handle errors if the file is not valid or cannot be opened.
        •	Implement B-tree Interaction Methods with Decorators:
        •	Use the @require_file_open decorator to ensure an index file is open before executing methods.
        •	Implement the following methods:
        •	insert_key_value: Insert a key/value pair into the B-tree.
        •	search_key: Search for a key in the B-tree.
        •	load_from_file: Load key/value pairs from a file into the B-tree.
        •	print_all: Print all key/value pairs in the B-tree.
        •	extract_to_file: Extract all key/value pairs from the B-tree to a file.
        •	Ensure each method handles exceptions and provides user feedback.

**Actions Taken:**

        1.	Implemented open_index_file Method:
        •	Checked if the specified file exists.
        •	Opened the file in binary read mode.
        •	Read and validated the magic number to ensure it’s a valid index file.
        •	Extracted the root block ID and next block ID from the file header.
        •	Initialized the B-tree with the current index file manager.
        •	Added error handling for IOError and FileFormatError.
        2.	Applied @require_file_open Decorator:
        •	Decorated methods that require an open index file to prevent execution if no file is open.
        •	Ensured the user is informed if they attempt to use these methods without an open file.
        3.	Implemented insert_key_value Method:
        •	Checked if the B-tree is initialized; if not, initialized it.
        •	Called the insert method on the B-tree to add the key/value pair.
        •	Handled DuplicateKeyError exceptions by logging and re-raising them.
        4.	Implemented search_key Method:
        •	Ensured the B-tree is initialized.
        •	Called the search method on the B-tree.
        •	Returned the value if found, or raised a KeyNotFoundError if not.
        5.	Implemented load_from_file Method:
        •	Checked if the specified file exists.
        •	Opened the file and read it line by line.
        •	Parsed each line to extract key/value pairs, skipping invalid lines.
        •	Performed batch insertion of valid key/value pairs.
        •	Provided feedback on invalid lines and duplicates.
        6.	Implemented print_all Method:
        •	Ensured the B-tree is initialized.
        •	Performed an in-order traversal of the B-tree to collect all key/value pairs.
        •	Printed the key/value pairs if any, or indicated that the B-tree is empty.
        7.	Implemented extract_to_file Method:
        •	Checked if the output file exists and prompted for overwrite confirmation.
        •	Collected all key/value pairs from the B-tree.
        •	Wrote the key/value pairs to the specified file.
        •	Handled IOError exceptions and informed the user of any issues. 

## December 1st 6:33 pm
### **Thoughts:**

The focus of this session was to implement the header update mechanism and finalize the `BTreeNode` class. The primary goal was to ensure that the B-Tree structure works seamlessly with file operations. This included creating nodes, writing to and reading from disk, inserting keys/values, splitting full nodes, and searching for keys.

---

### **Plan:**

1. **Update Header Mechanism:**
   - Implement a method to update the index file's header block with the root block and next block information whenever structural changes occur in the B-Tree.

2. **Complete `BTreeNode` Class:**
   - Implement methods for:
     - Reading and writing nodes to disk.
     - Inserting key-value pairs into non-full nodes.
     - Splitting full nodes during insertion.
     - Searching for keys within a node and its children.

3. **Implement Error Handling:**
   - Add robust error handling for file I/O operations.
   - Handle cases like duplicate keys, incomplete block reads, and invalid node data.

4. **Test the Code:**
   - Test all implemented methods for various edge cases, including full nodes, leaf and non-leaf nodes, and invalid inputs.

---

### **Actions Taken:**

#### **1. Header Update Implementation:**
    1.Implemented `update_header` in `IndexFileManager` to keep the file's header synchronized with changes to the B-Tree structure.
    2. BTreeNode Initialization:
	    •Added the BTreeNode class to manage nodes in the B-Tree. Nodes are initialized either as new nodes or by loading from an existing file block
    3. Node Read and Write:
	    • Implemented _write_node to serialize node data and save it to the appropriate block in the file.
	    • Implemented _read_node to deserialize node data from the file.
    4. Insertion and Splitting:

	    • Implemented insert_non_full to handle insertion of a key-value pair into non-full nodes.
        • Implemented split_child to split full nodes and propagate keys to parent nodes.
    5. Search Operation:
	    • Added a recursive search method to locate keys within a node or its children.


## December 1st 8:42 pm
### **Thoughts:**

To complete the B-Tree implementation, the focus of this session was on traversal, insertion, and managing the root node of the B-Tree. The `traverse` method ensures in-order traversal of the tree, while the `insert` method manages adding new key-value pairs, including handling cases where the root node is full and needs to split. This is a critical part of maintaining the B-Tree's structural properties.
### **Plan:**

1. **Traversal Implementation:**
   - Add a method to perform an in-order traversal of the B-Tree, collecting all key-value pairs.
   - Ensure the method correctly handles both leaf and non-leaf nodes.

2. **B-Tree Insertion Logic:**
   - Manage the root node during insertions:
     - Handle cases where the root is empty (tree is being initialized).
     - Handle cases where the root is full and needs to split.
   - Ensure the B-Tree properties are maintained during insertions.

3. **Testing and Error Handling:**
   - Test traversal for edge cases such as empty trees, single-node trees, and deeper trees.
   - Validate insertion logic for both leaf and non-leaf nodes, including root splits.
### **Actions Taken:**
#### **1. Implemented Traversal:**
- Created the `traverse` method in `BTreeNode` to perform an in-order traversal:
  - Recursively visited child nodes in sorted order.
  - Collected all key-value pairs into a provided result list.
  ```python
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
#### **2. Root Node Management in B-Tree:**

	•	Added logic to the BTree class to initialize the root node if it is empty:
	•	Created a new BTreeNode and updated the header.
	•	Handled the case where the root node is full:
	•	Split the root node into two child nodes.
	•	Created a new root node to accommodate the split key.

### **Code Changes:**

	1.	Traversal in BTreeNode:
	•	Added the traverse method to recursively collect key-value pairs in sorted order.
	•	Ensured the method handles leaf and non-leaf nodes correctly.
	2.	B-Tree Insertion in BTree:
	•	Managed the initialization of the root node when inserting into an empty tree.
	•	Handled splitting of a full root node and updated the header accordingly.

## December 1st 9:32 pm
### **Thoughts:**

In this session, the focus was on finalizing key functionalities for the `BTree` class and ensuring proper integration with the main program. The addition of `search` and `traverse` methods ensures that the tree can handle lookups and traversals efficiently. The `main` function serves as the entry point for the program, linking the `IndexFileManager` and `CommandHandler` to provide an interactive user interface.
### **Plan:**

1. **Search Implementation:**
   - Add a method to search for a key in the B-Tree starting from the root node.
   - Ensure recursive calls are managed through the `BTreeNode` class.

2. **Traversal Integration:**
   - Implement a method to traverse the entire B-Tree and collect key-value pairs in sorted order.
   - Ensure this method integrates well with the `traverse` method in `BTreeNode`.

3. **Main Functionality:**
   - Create a `main` function to initialize the program.
   - Link the `IndexFileManager` and `CommandHandler` for user interaction.
   - Set up the program to start from the `main` function when executed.

4. **Testing:**
   - Verify that search operations return correct results for existing and non-existing keys.
   - Validate traversal outputs for trees of varying depths and structures.

### **Actions Taken:**

#### **1. Search Functionality:**
- Implemented the `search` method in the `BTree` class to handle lookups:
  - Checked if the tree is empty.
  - If not, delegated the search to the root node.
  ```python
  def search(self, key):
      """Searches for a key in the B-tree."""
      if self.root is None:
          return None
      else:
          return self.root.search(key)
#### **2. Traversal Integration:**

	•	Added the traverse method to the BTree class:
	•	Delegated the traversal to the root node.
	•	Collected all key-value pairs in sorted order for further processing or display.

#### **3. Main Functionality:**

	•	Created a main function to serve as the program’s entry point:
	•	Initialized the IndexFileManager and CommandHandler.
	•	Started the command loop for user interaction.

## December 1st 9:40 pm

	Indentation Corrections:
	•	Ensured that all class and method definitions have consistent indentation.
	•	Fixed indentation levels within methods, especially in loops and conditional statements.
	•	Made sure decorators like @require_file_open are properly aligned with the methods they decorate.
	•	Code Cleanup:
	•	Removed any unnecessary comments or repeated code.
	•	Verified that all methods and functions are correctly defined and closed.
	•	Ensured that the code follows PEP 8 styling guidelines where possible.
	•	Syntax Corrections:
	•	Checked for missing colons (:) after class and function definitions.
	•	Made sure all parentheses and brackets are properly closed.
	•	Fixed variable names and ensured consistency throughout the code.
	•	Error Handling:
	•	Verified that all exceptions are properly caught and handled.
	•	Ensured that user feedback is provided where appropriate.
	•	Functionality Verification:
	•	Made sure that the main function is correctly defined and that the program starts as expected.
	•	Confirmed that all required methods are present in the BTreeNode and BTree classes.

## December 1st 9:50pm 

    - Created Readme.md file and updated with required notes for TA 
    