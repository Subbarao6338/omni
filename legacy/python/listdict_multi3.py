import datetime
import os

class ListDictsManager:
    """
    A class to manage lists and dictionaries with logging and reporting features.
    """

    def __init__(self):
        """
        Initializes the ListDictsManager with empty lists and dictionaries,
        and sets up logging.
        """
        self.lists = {}
        self.dicts = {}
        self.log_file = "operations_log.txt"
        self.list_create_count = 0
        self.dict_create_count = 0
        self.list_add_count = 0
        self.list_edit_count = 0
        self.list_remove_count = 0
        self.dict_add_count = 0
        self.dict_edit_count = 0
        self.dict_remove_count = 0
        self.operation_stack = []
        self.initialize_log_file()

    def initialize_log_file(self):
        """Initializes the log file."""
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as log:
                log.write("Log file created.\n")

    def log_operation(self, operation, key=None, count=0, items=None):
        """Logs operations performed on lists and dictionaries."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}, {operation}, {key}, Count: {count}"
        if items:
            log_entry += f", Items: {items}"
        log_entry += "\n"

        if count > 0:
            log_entry = f"{timestamp}, {operation}, {key}, Count: {count}\n"
        else:
            log_entry = f"{timestamp}, {operation}, {key}\n"
        with open(self.log_file, "a") as log:
            log.write(log_entry)
        self.operation_stack.append((operation, key, count, items))

    def display_lists(self):
        """Displays all current lists."""
        print("Current Lists: ")
        for name, lst in self.lists.items():
            print(f"{name} (Items: {len(lst)}): {lst}")

    def display_dicts(self):
        """Displays all current dictionaries."""
        print("Current Dictionaries: ")
        for name, dct in self.dicts.items():
            print(f"{name} (Items: {len(dct)}): {dct}")

    def create_list(self):
        """Creates a new list with a user-defined name."""
        name = input("Enter name for new list: ").strip()
        if not name:
            print("List name cannot be empty.")
            return
        if name in self.lists:
            print("List with this name already exists.")
        else:
            self.lists[name] = []
            self.list_create_count += 1
            self.log_operation("Create List", name)
            print("List created successfully.")

    def create_dict(self):
        """Creates a new dictionary with a user-defined name."""
        name = input("Enter name for new dictionary: ").strip()
        if not name:
            print("Dictionary name cannot be empty.")
            return
        if name in self.dicts:
            print("Dictionary with this name already exists.")
        else:
            self.dicts[name] = {}
            self.dict_create_count += 1
            self.log_operation("Create Dictionary", name)
            print("Dictionary created successfully.")

    def add_to_list(self):
        """Adds items to an existing list."""
        self.display_lists()
        name = input("Enter name of list to add to: ")
        if name in self.lists:
            try:
                new_items = int(input("Enter the number of items to add: "))
                for _ in range(new_items):
                    item = input("Enter item to add to list: ")
                    self.lists[name].append(item)
                self.list_add_count += new_items
                self.log_operation("Add to List", name, new_items)
                print(f"{new_items} item(s) added to the list successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("List not found.")

    def add_to_dict(self):
        """Adds key-value pairs to an existing dictionary."""
        self.display_dicts()
        name = input("Enter name of dictionary to add to: ")
        if name in self.dicts:
            try:
                new_items = int(input("Enter the number of items to add: "))
                for _ in range(new_items):
                    key = input("Enter key for dictionary: ")
                    value = input("Enter value for dictionary: ")
                    self.dicts[name][key] = value
                self.dict_add_count += new_items
                self.log_operation("Add to Dictionary", name, new_items)
                print(f"{new_items} item(s) added to the dictionary successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Dictionary not found.")

    def edit_in_list(self):
        """Edits an item in an existing list."""
        self.display_lists()
        name = input("Enter name of list to edit: ")
        if name in self.lists:
            try:
                index = self.get_valid_index(self.lists[name])
                new_item = input("Enter new item: ")
                self.lists[name][index] = new_item
                self.list_edit_count += 1
                self.log_operation("Edit in List", name)
                print("Item edited in list successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("List not found.")

    def edit_in_dict(self):
        """Edits a value in an existing dictionary."""
        self.display_dicts()
        name = input("Enter name of dictionary to edit: ")
        if name in self.dicts:
            key = input("Enter key of item to edit: ")
            if key in self.dicts[name]:
                new_value = input("Enter new value: ")
                self.dicts[name][key] = new_value
                self.dict_edit_count += 1
                self.log_operation("Edit in Dictionary", name)
                print("Item edited in dictionary successfully.")
            else:
                print("Key not found in dictionary.")
        else:
            print("Dictionary not found.")

    def remove_from_list(self):
        """Removes an item from an existing list."""
        self.display_lists()
        name = input("Enter name of list to remove from: ")
        if name in self.lists:
            try:
                index = self.get_valid_index(self.lists[name])
                del self.lists[name][index]
                self.list_remove_count += 1
                self.log_operation("Remove from List", name)
                print("Item removed from list successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("List not found.")

    def remove_from_dict(self):
        """Removes a key-value pair from an existing dictionary."""
        self.display_dicts()
        name = input("Enter name of dictionary to remove from: ")
        if name in self.dicts:
            key = input("Enter key of item to remove: ")
            if key in self.dicts[name]:
                del self.dicts[name][key]
                self.dict_remove_count += 1
                self.log_operation("Remove from Dictionary", name)
                print("Item removed from dictionary successfully.")
            else:
                print("Key not found in dictionary.")
        else:
            print("Dictionary not found.")

    def delete_list(self):
        """Deletes an entire list."""
        self.display_lists()
        name = input("Enter name of list to delete: ")
        if name in self.lists:
            del self.lists[name]
            self.log_operation("Delete List", name)
            print("List deleted successfully.")
        else:
            print("List not found.")

    def delete_dict(self):
        """Deletes an entire dictionary."""
        self.display_dicts()
        name = input("Enter name of dictionary to delete: ")
        if name in self.dicts:
            del self.dicts[name]
            self.log_operation("Delete Dictionary", name)
            print("Dictionary deleted successfully.")
        else:
            print("Dictionary not found.")

    def undo_last_operation(self):
        """Undoes the last operation performed."""
        if not self.operation_stack:
            print("No operations to undo.")
            return

        last_operation = self.operation_stack.pop()
        operation, key, count, items = last_operation

        if operation == "Create List":
            del self.lists[key]
            self.list_create_count -= 1
        elif operation == "Create Dictionary":
            del self.dicts[key]
            self.dict_create_count -= 1
        elif operation == "Add to List":
            self.lists[key] = self.lists[key][:-count]
            self.list_add_count -= count
        elif operation == "Add to Dictionary":
            for _ in range(count):
                for item in items:
                    # Logic to remove the last added key-value pair
                    if item in self.dicts[key]:
                        del self.dicts[key][item]
            self.dict_add_count -= count
        # Handle other operations similarly...

        print(f"Undid last operation: {operation} on {key}.")

    def generate_report(self):
        """Generates a report of operations performed."""
        try:
            with open(self.log_file, "r") as log:
                operations = log.readlines()
                print("\nDaily Operations Report:")
                print("\nOperation Counts:")
                print(f"List Creations: {self.list_create_count}")
                print(f"List Additions: {self.list_add_count}")
                print(f"List Edits: {self.list_edit_count}")
                print(f"List Removals: {self.list_remove_count}")
                print(f"Dictionary Creations: {self.dict_create_count}")
                print(f"Dictionary Additions: {self.dict_add_count}")
                print(f"Dictionary Edits: {self.dict_edit_count}")
                print(f"Dictionary Removals: {self.dict_remove_count}")

                print(f"Total operations performed: {len(operations)}")
                print("\nDetailed Operations:")
                for operation in operations:
                    print(operation.strip())
                print("\nSummary of Changes:")
                print(f"Total Items in List: {len(self.lists)}")
                print(f"Total Items in Dictionary: {len(self.dicts)}")

        except FileNotFoundError:
            print("Log file not found.")

    def get_valid_index(self, lst):
        """Gets a valid index from the user for the given list."""
        while True:
            try:
                index = int(input("Enter index: "))
                if 0 <= index < len(lst):
                    return index
                else:
                    print("Invalid index. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")

    def search_in_list(self):
        """Searches for an item in a list."""
        self.display_lists()
        name = input("Enter name of list to search in: ")
        if name in self.lists:
            item = input("Enter item to search for: ")
            if item in self.lists[name]:
                print(f"Item '{item}' found in list '{name}'.")
            else:
                print(f"Item '{item}' not found in list '{name}'.")
        else:
            print("List not found.")

    def search_in_dict(self):
        """Searches for a key in a dictionary."""
        self.display_dicts()
        name = input("Enter name of dictionary to search in: ")
        if name in self.dicts:
            key = input("Enter key to search for: ")
            if key in self.dicts[name]:
                print(f"Key '{key}' found in dictionary '{name}' with value: {self.dicts[name][key]}.")
            else:
                print(f"Key '{key}' not found in dictionary '{name}'.")
        else:
            print("Dictionary not found.")

    def sort_list(self):
        """Sorts an existing list."""
        self.display_lists()
        name = input("Enter name of list to sort: ")
        if name in self.lists:
            self.lists[name].sort()
            self.log_operation("Sort List", name)
            print(f"List '{name}' sorted successfully.")
        else:
            print("List not found.")

    def sort_dict(self):
        """Sorts an existing dictionary by keys."""
        self.display_dicts()
        name = input("Enter name of dictionary to sort by keys: ")
        if name in self.dicts:
            sorted_dict = dict(sorted(self.dicts[name].items()))
            self.dicts[name] = sorted_dict
            self.log_operation("Sort Dictionary", name)
            print(f"Dictionary '{name}' sorted by keys successfully.")
        else:
            print("Dictionary not found.")

    def clear_list(self):
        """Clears all items from an existing list."""
        self.display_lists()
        name = input("Enter name of list to clear: ")
        if name in self.lists:
            self.lists[name].clear()
            self.log_operation("Clear List", name)
            print(f"List '{name}' cleared successfully.")
        else:
            print("List not found.")

    def clear_dict(self):
        """Clears all items from an existing dictionary."""
        self.display_dicts()
        name = input("Enter name of dictionary to clear: ")
        if name in self.dicts:
            self.dicts[name].clear()
            self.log_operation("Clear Dictionary", name)
            print(f"Dictionary '{name}' cleared successfully.")
        else:
            print("Dictionary not found.")

    def display_help(self):
        """Displays help information for using the program."""
        print("Help Menu:")
        print("1. Display Lists: Show all current lists.")
        print("2. Display Dictionaries: Show all current dictionaries.")
        print("3. Create List: Create a new list.")
        print("4. Create Dictionary: Create a new dictionary.")
        print("5. Add to List: Add items to an existing list.")
        print("6. Add to Dictionary: Add key-value pairs to an existing dictionary.")
        print("7. Edit in List: Edit an item in an existing list.")
        print("8. Edit in Dictionary: Edit a value in an existing dictionary.")
        print("9. Remove from List: Remove an item from an existing list.")
        print("10. Remove from Dictionary: Remove a key-value pair from an existing dictionary.")
        print("11. Delete List: Delete an entire list.")
        print("12. Delete Dictionary: Delete an entire dictionary.")
        print("13. Generate Report: Generate a report of operations.")
        print("14. Undo Last Operation: Undo the last performed operation.")
        print("15. Search in List: Search for an item in a list.")
        print("16. Search in Dictionary: Search for a key in a dictionary.")
        print("17. Sort List: Sort an existing list.")
        print("18. Sort Dictionary: Sort an existing dictionary by keys.")
        print("19. Clear List: Clear all items from a list.")
        print("20. Clear Dictionary: Clear all items from a dictionary.")
        print("21. Help: Display this help menu.")
        print("22. Exit: Exit the program.")

    def handle_choice(self, choice):
        if choice == "1":
            self.display_lists()
        elif choice == "2":
            self.display_dicts()
        elif choice == "3":
            self.create_list()
        elif choice == "4":
            self.create_dict()
        elif choice == "5":
            self.add_to_list()
        elif choice == "6":
            self.add_to_dict()
        elif choice == "7":
            self.edit_in_list()
        elif choice == "8":
            self.edit_in_dict()
        elif choice == "9":
            self.remove_from_list()
        elif choice == "10":
            self.remove_from_dict()
        elif choice == "11":
            self.delete_list()
        elif choice == "12":
            self.delete_dict()
        elif choice == "13":
            self.generate_report()
        elif choice == "14":
            self.undo_last_operation()
        elif choice == "15":
            self.search_in_list()
        elif choice == "16":
            self.search_in_dict()
        elif choice == "17":
            self.sort_list()
        elif choice == "18":
            self.sort_dict()
        elif choice == "19":
            self.clear_list()
        elif choice == "20":
            self.clear_dict()
        elif choice == "21":
            self.display_help()
        elif choice == "22":
            confirm_exit = input("Are you sure you want to exit? (yes/no): ").strip().lower()
            if confirm_exit == "yes":
                print("Exiting the program. Goodbye!")
                # Perform any necessary cleanup here if needed
                exit()
            else:
                print("Exit canceled. Returning to the main menu.")

        else:
            print("Invalid choice. Please try again.")

# Main loop for user interaction
if __name__ == "__main__":
    try:
        manager = ListDictsManager()
        while True:
            print("\nMain Menu:")
            print("1. Display Lists")
            print("2. Display Dictionaries")
            print("3. Create List")
            print("4. Create Dictionary")
            print("5. Add to List")
            print("6. Add to Dictionary")
            print("7. Edit in List")
            print("8. Edit in Dictionary")
            print("9. Remove from List")
            print("10. Remove from Dictionary")
            print("11. Delete List")
            print("12. Delete Dictionary")
            print("13. Generate Report")
            print("14. Undo Last Operation")
            print("15. Search in List")
            print("16. Search in Dictionary")
            print("17. Sort List")
            print("18. Sort Dictionary")
            print("19. Clear List")
            print("20. Clear Dictionary")
            print("21. Help")
            print("22. Exit")

            choice = input("Enter your choice: ")
            manager.handle_choice(choice)

    except Exception as e:
        print("Error:", e)
