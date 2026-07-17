import sqlite3


def connect_db():
    conn = sqlite3.connect('products.db')
    return conn


def create_table(conn):
    table_name = input("Enter the table name: ")
    columns = input("Enter the columns (e.g., name TEXT, price REAL, quantity INTEGER): ")
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {columns})''')
    conn.commit()
    print(f"Table '{table_name}' created successfully.")


def insert_data(conn):
    table_name = input("Enter the table name to insert data into: ")
    cursor = conn.cursor()

    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]

    values = []
    for column in columns[1:]:  # Skip the 'id' column
        value = input(f"Enter value for {column}: ")
        values.append(value)

    cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns[1:])}) VALUES ({', '.join(['?' for _ in values])})",
                   values)
    conn.commit()
    print("Product inserted successfully.")


def view_data(conn):
    table_name = input("Enter the table name to view data from: ")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    print("Current products:")
    for row in rows:
        print(row)


def update_data(conn):
    table_name = input("Enter the table name to update data in: ")
    product_id = int(input("Enter the ID of the product to update: "))
    cursor = conn.cursor()

    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]

    values = []
    for column in columns[1:]:  # Skip the 'id' column
        new_value = input(f"Enter new value for {column} (leave blank to keep current value): ")
        if new_value:
            values.append(new_value)
        else:
            values.append(None)

    # Update only the columns that have new values
    set_clause = ', '.join([f"{columns[i + 1]} = ?" for i in range(len(values)) if values[i] is not None])
    update_values = [values[i] for i in range(len(values)) if values[i] is not None]

    if set_clause:
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE id = ?", (*update_values, product_id))
        conn.commit()
        print("Product updated successfully.")
    else:
        print("No updates made.")


def delete_data(conn):
    table_name = input("Enter the table name to delete data from: ")
    product_id = int(input("Enter the ID of the product to delete: "))
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (product_id,))
    conn.commit()
    print("Product deleted successfully.")


def main():
    conn = connect_db()

    while True:
        print("\nMenu:")
        print("1. Create Table")
        print("2. Insert Product")
        print("3. View Products")
        print("4. Update Product")
        print("5. Delete Product")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_table(conn)
        elif choice == '2':
            insert_data(conn)
        elif choice == '3':
            view_data(conn)
        elif choice == '4':
            update_data(conn)
        elif choice == '5':
            delete_data(conn)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

    conn.close()


if __name__ == "__main__":
    main()
