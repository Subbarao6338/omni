class ListDictsManager:
    def __init__(self):
        self.lists = {}
        self.dicts = {}

    def display_lists(self):
        print("Current Lists: ")
        for name, lst in self.lists.items():
            print(f"{name}: {lst}")

    def display_dicts(self):
        print("Current Dictionaries: ")
        for name, dct in self.dicts.items():
            print(f"{name}: {dct}")

    def create_list(self):
        name = input("Enter name for new list: ")
        if name in self.lists:
            print("List with this name already exists.")
        else:
            self.lists[name] = []
            print("List created successfully.")

    def create_dict(self):
        name = input("Enter name for new dictionary: ")
        if name in self.dicts:
            print("Dictionary with this name already exists.")
        else:
            self.dicts[name] = {}
            print("Dictionary created successfully.")

    def add_to_list(self):
        self.display_lists()
        name = input("Enter name of list to add to: ")
        if name in self.lists:
            try:
                new_items = int(input("Enter the number of items to add: "))
                for i in range(new_items):
                    item = input("Enter item to add to list: ")
                    self.lists[name].append(item)
                print(f"{new_items} item(s) added to the list successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("List not found.")

    def add_to_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to add to: ")
        if name in self.dicts:
            try:
                new_items = int(input("Enter the number of items to add: "))
                for i in range(new_items):
                    key = input("Enter key for dictionary: ")
                    value = input("Enter value for dictionary: ")
                    self.dicts[name][key] = value
                print(f"{new_items} item(s) added to the dictionary successfully.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Dictionary not found.")

    def edit_in_list(self):
        self.display_lists()
        name = input("Enter name of list to edit: ")
        if name in self.lists:
            try:
                index = int(input("Enter index of item to edit: "))
                if 0 <= index < len(self.lists[name]):
                    new_item = input("Enter new item: ")
                    self.lists[name][index] = new_item
                    print("Item edited in list successfully.")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("List not found.")

    def edit_in_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to edit: ")
        if name in self.dicts:
            try:
                key = input("Enter key of item to edit: ")
                if key in self.dicts[name]:
                    new_value = input("Enter new value: ")
                    self.dicts[name][key] = new_value
                    print("Item edited in dictionary successfully.")
                else:
                    print("Key not found in dictionary.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("Dictionary not found.")

    def remove_from_list(self):
        self.display_lists()
        name = input("Enter name of list to remove from: ")
        if name in self.lists:
            try:
                index = int(input("Enter index of item to remove: "))
                if 0 <= index < len(self.lists[name]):
                    del self.lists[name][index]
                    print("Item removed from list successfully.")
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("List not found.")

    def remove_from_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to remove from: ")
        if name in self.dicts:
            try:
                key = input("Enter key of item to remove: ")
                if key in self.dicts[name]:
                    del self.dicts[name][key]
                    print("Item removed from dictionary successfully.")
                else:
                    print("Key not found in dictionary.")
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        else:
            print("Dictionary not found.")

    def delete_list(self):
        self.display_lists()
        name = input("Enter name of list to delete: ")
        if name in self.lists:
            del self.lists[name]
            print("List deleted successfully.")
        else:
            print("List not found.")

    def delete_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to delete: ")
        if name in self.dicts:
            del self.dicts[name]
            print("Dictionary deleted successfully.")
        else:
            print("Dictionary not found.")

try:
    manager = ListDictsManager()
    while True:
        print("\n1. Display Lists")
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
        print("13. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            manager.display_lists()
        elif choice == "2":
            manager.display_dicts()
        elif choice == "3":
            manager.create_list()
        elif choice == "4":
            manager.create_dict()
        elif choice == "5":
            manager.add_to_list()
        elif choice == "6":
            manager.add_to_dict()
        elif choice == "7":
            manager.edit_in_list()
        elif choice == "8":
            manager.edit_in_dict()
        elif choice == "9":
            manager.remove_from_list()
        elif choice == "10":
            manager.remove_from_dict()
        elif choice == "11":
            manager.delete_list()
        elif choice == "12":
            manager.delete_dict()
        elif choice == "13":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

except Exception as e:
    print("Error:", e)
