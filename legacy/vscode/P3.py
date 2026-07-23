#1 single

class ListDictManager:
    def __init__(self):
        self.my_list = []
        self.my_dict = {}

    def display_list(self):
        print("Current List: ", self.my_list)

    def display_dict(self):
        print("Current Dictionary: ", self.my_dict)

    # def add_to_list(self):
    #     item = input("Enter item to add to list: ")
    #     self.my_list.append(item)
    #     print("Item added to list successfully.")

    def add_to_list(self):
        new_items = int(input("Enter the number of items to add: "))
        for i in range(new_items):
            item=input("Enter item to add to list: ")
            self.my_list.append((item))
        print("Item added to list successfully.")

    # def add_to_dict(self):
    #     key = input("Enter key for dictionary: ")
    #     value = input("Enter value for dictionary: ")
    #     self.my_dict[key] = value
    #     print("Item added to dictionary successfully.")

    def add_to_dict(self):
        new_items = int(input("Enter the number of items to add: "))
        for i in range(new_items):
            key = input("Enter key for dictionary: ")
            value = input("Enter value for dictionary: ")
            self.my_dict[key] = value
        print("Items added to dictionary successfully.")

    def edit_in_list(self):
        self.display_list()
        index = int(input("Enter index of item to edit: "))
        if index < len(self.my_list):
            new_item = input("Enter new item: ")
            self.my_list[index] = new_item
            print("Item edited in list successfully.")
        else:
            print("Invalid index.")

    def edit_in_dict(self):
        self.display_dict()
        key = input("Enter key of item to edit: ")
        if key in self.my_dict:
            new_value = input("Enter new value: ")
            self.my_dict[key] = new_value
            print("Item edited in dictionary successfully.")
        else:
            print("Key not found in dictionary.")

    def remove_from_list(self):
        self.display_list()
        index = int(input("Enter index of item to remove: "))
        if index < len(self.my_list):
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

def lds():
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
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    lds()

#2 multiple

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
        self.lists[name] = []
        print("List created successfully.")

    def create_dict(self):
        name = input("Enter name for new dictionary: ")
        self.dicts[name] = {}
        print("Dictionary created successfully.")

    def add_to_list(self):
        self.display_lists()
        name = input("Enter name of list to add to: ")
        if name in self.lists:
            new_items = int(input("Enter the number of items to add: "))
            for i in range(new_items):
                item = input("Enter item to add to list: ")
                self.lists[name].append(item)
            print("Item added to list successfully.")
        else:
            print("List not found.")

    def add_to_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to add to: ")
        if name in self.dicts:
            new_items = int(input("Enter the number of items to add: "))
            for i in range(new_items):
                key = input("Enter key for dictionary: ")
                value = input("Enter value for dictionary: ")
                self.dicts[name][key] = value
            print("Items added to dictionary successfully.")
        else:
            print("Dictionary not found.")

    def edit_in_list(self):
        self.display_lists()
        name = input("Enter name of list to edit: ")
        if name in self.lists:
            index = int(input("Enter index of item to edit: "))
            if index < len(self.lists[name]):
                new_item = input("Enter new item: ")
                self.lists[name][index] = new_item
                print("Item edited in list successfully.")
            else:
                print("Invalid index.")
        else:
            print("List not found.")

    def edit_in_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to edit: ")
        if name in self.dicts:
            key = input("Enter key of item to edit: ")
            if key in self.dicts[name]:
                new_value = input("Enter new value: ")
                self.dicts[name][key] = new_value
                print("Item edited in dictionary successfully.")
            else:
                print("Key not found in dictionary.")
        else:
            print("Dictionary not found.")

    def remove_from_list(self):
        self.display_lists()
        name = input("Enter name of list to remove from: ")
        if name in self.lists:
            index = int(input("Enter index of item to remove: "))
            if index < len(self.lists[name]):
                del self.lists[name][index]
                print("Item removed from list successfully.")
            else:
                print("Invalid index.")
        else:
            print("List not found.")

    def remove_from_dict(self):
        self.display_dicts()
        name = input("Enter name of dictionary to remove from: ")
        if name in self.dicts:
            key = input("Enter key of item to remove: ")
            if key in self.dicts[name]:
                del self.dicts[name][key]
                print("Item removed from dictionary successfully.")
            else:
                print("Key not found in dictionary.")
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

def ldm():
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
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    ldm()


#3

# lists = {}
# dicts = {}
#
# def display_lists():
#     print("Current Lists: ")
#     for name, lst in lists.items():
#         print(f"{name}: {lst}")
#
# def display_dicts():
#     print("Current Dictionaries: ")
#     for name, dct in dicts.items():
#         print(f"{name}: {dct}")
#
# def create_list():
#     name = input("Enter name for new list: ")
#     lists[name] = []
#     print("List created successfully.")
#
# def create_dict():
#     name = input("Enter name for new dictionary: ")
#     dicts[name] = {}
#     print("Dictionary created successfully.")
#
# def add_to_list():
#     display_lists()
#     name = input("Enter name of list to add to: ")
#     if name in lists:
#         item = input("Enter item to add to list: ")
#         lists[name].append(item)
#         print("Item added to list successfully.")
#     else:
#         print("List not found.")
#
# def add_to_dict():
#     display_dicts()
#     name = input("Enter name of dictionary to add to: ")
#     if name in dicts:
#         key = input("Enter key for dictionary: ")
#         value = input("Enter value for dictionary: ")
#         dicts[name][key] = value
#         print("Item added to dictionary successfully.")
#     else:
#         print("Dictionary not found.")
#
# def main():
#     while True:
#         print("\n1. Display Lists")
#         print("2. Display Dictionaries")
#         print("3. Create List")
#         print("4. Create Dictionary")
#         print("5. Add to List")
#         print("6. Add to Dictionary")
#         print("7. Exit")
#         choice = input("Enter your choice: ")
#         if choice == "1":
#             display_lists()
#         elif choice == "2":
#             display_dicts()
#         elif choice == "3":
#             create_list()
#         elif choice == "4":
#             create_dict()
#         elif choice == "5":
#             add_to_list()
#         elif choice == "6":
#             add_to_dict()
#         elif choice == "7":
#             break
#         else:
#             print("Invalid choice. Please try again.")
#
# if __name__ == "__main__":
#     main()

