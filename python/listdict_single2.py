import datetime
import os

class ListDictManager:
    def __init__(self):
        self.my_list = []
        self.my_dict = {}
        self.log_file = "operations_log.txt"
        self.list_add_count = 0  # Counter for list additions
        self.list_edit_count = 0  # Counter for list edits
        self.list_remove_count = 0  # Counter for list removals
        self.dict_add_count = 0  # Counter for dictionary additions
        self.dict_edit_count = 0  # Counter for dictionary edits
        self.dict_remove_count = 0  # Counter for dictionary removals
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as log:
                log.write("Log file created.\n")

    def log_operation(self, operation, key=None):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as log:
            log.write(f"{timestamp}, {operation}, {key}\n")

    def display_list(self):
        print("Current List: ", self.my_list)

    def display_dict(self):
        print("Current Dictionary: ", self.my_dict)

    def add_to_list(self):
        try:
            new_items = int(input("Enter the number of items to add: "))
            for i in range(new_items):
                item = input("Enter item to add to list: ")
                self.my_list.append(item)
                self.log_operation("add_to_list", item)
            self.list_add_count += new_items  # Increment the add count
            print(f"{new_items} item(s) added to the list successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def add_to_dict(self):
        try:
            new_items = int(input("Enter the number of items to add: "))
            for i in range(new_items):
                key = input("Enter key for dictionary: ")
                value = input("Enter value for dictionary: ")
                self.my_dict[key] = value
                self.log_operation("add_to_dict", key)
            self.dict_add_count += new_items  # Increment the add count
            print(f"{new_items} item(s) added to the dictionary successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def edit_in_list(self):
        self.display_list()
        try:
            index = int(input("Enter index of item to edit: "))
            if 0 <= index < len(self.my_list):
                new_item = input("Enter new item: ")
                old_item = self.my_list[index]
                self.my_list[index] = new_item
                self.log_operation("edit_in_list", f"Index: {index}, Old: {old_item}, New: {new_item}")
                self.list_edit_count += 1  # Increment the edit count
                print("Item edited in list successfully.")
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

    def edit_in_dict(self):
        self.display_dict()
        try:
            key = input("Enter key of item to edit: ")
            if key in self.my_dict:
                old_value = self.my_dict[key]
                new_value = input("Enter new value: ")
                self.my_dict[key] = new_value
                self.log_operation("edit_in_dict", f"Key: {key}, Old: {old_value}, New: {new_value}")
                self.dict_edit_count += 1  # Increment the edit count
                print("Item edited in dictionary successfully.")
            else:
                print("Key not found in dictionary.")
        except ValueError:
            print("Invalid input. Please enter a valid key.")

    def remove_from_list(self):
        self.display_list()
        try:
            index = int(input("Enter index of item to remove: "))
            if 0 <= index < len(self.my_list):
                removed_item = self.my_list[index]
                del self.my_list[index]
                self.log_operation("remove_from_list", f"Index: {index}, Item: {removed_item}")
                self.list_remove_count += 1  # Increment the remove count
                print("Item removed from list successfully.")
            else:
                print("Invalid index.")
        except ValueError:
            print("Invalid input. Please enter a valid index.")

    def remove_from_dict(self):
        self.display_dict()
        key = input("Enter key of item to remove: ")
        if key in self.my_dict:
            removed_value = self.my_dict[key]
            del self.my_dict[key]
            self.log_operation("remove_from_dict", f"Key: {key}, Value: {removed_value}")
            self.dict_remove_count += 1  # Increment the remove count
            print("Item removed from dictionary successfully.")
        else:
            print("Key not found in dictionary.")

    def generate_report(self):
        try:
            with open(self.log_file, "r") as log:
                operations = log.readlines()
                print("\nDaily Operations Report:")
                print("\nOperation Counts:")
                print(f"List Additions: {self.list_add_count}")
                print(f"List Edits: {self.list_edit_count}")
                print(f"List Removals: {self.list_remove_count}")
                print(f"Dictionary Additions: {self.dict_add_count}")
                print(f"Dictionary Edits: {self.dict_edit_count}")
                print(f"Dictionary Removals: {self.dict_remove_count}")
                print(f"Total operations performed: {len(operations)}")
                for operation in operations:
                    print(operation.strip())
        except FileNotFoundError:
            print("Log file not found.")

try:
    manager = ListDictManager()
    while True:
        print("\n1. Display List")
        print("2. Display Dictionary")
        print("3. Add to List")
        print("4. Add to Dictionary")
        print("5. Edit in List")
        print("6. Edit in Dictionary")
        print("7. Remove from List")
        print("8. Remove from Dictionary")
        print("9. Generate Daily Report")
        print("10. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            manager.display_list()
        elif choice == "2":
            manager.display_dict()
        elif choice == "3":
            manager.add_to_list()
        elif choice == "4":
            manager.add_to_dict()
        elif choice == "5":
            manager.edit_in_list()
        elif choice == "6":
            manager.edit_in_dict()
        elif choice == "7":
            manager.remove_from_list()
        elif choice == "8":
            manager.remove_from_dict()
        elif choice == "9":
            manager.generate_report()
        elif choice == "10":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

except Exception as e:
    print("Error:", e)