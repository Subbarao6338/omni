class ListDictManager:
    def __init__(self):
        self.my_list = []
        self.my_dict = {}

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
            print(f"{new_items} item(s) added to the dictionary successfully.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def edit_in_list(self):
        self.display_list()
        try:
            index = int(input("Enter index of item to edit: "))
            if 0 <= index < len(self.my_list):
                new_item = input("Enter new item: ")
                self.my_list[index] = new_item
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
                new_value = input("Enter new value: ")
                self.my_dict[key] = new_value
                print("Item edited in dictionary successfully.")
            else:
                print("Key not found in dictionary.")
        except ValueError:
            print("Invalid input. Please enter a valid key.")

    def remove_from_list(self):
        self.display_list()
        index = int(input("Enter index of item to remove: "))
        if 0 <= index < len(self.my_list):
            del self.my_list[index]
            print("Item removed from list successfully.")
        else:
            print("Invalid index.")

    def remove_from_dict(self):
        self.display_dict()
        key = input("Enter key of item to remove: ")
        if key in self.my_dict:
            del self.my_dict[key]
            print("Item removed from dictionary successfully.")
        else:
            print("Key not found in dictionary.")

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
        print("9. Exit")
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
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

except Exception as e:
    print("Error:", e)
