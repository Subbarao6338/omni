import sqlite3


def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn


def create_table(conn, table_name, columns):
    cursor = conn.cursor()
    columns_with_types = ', '.join([f"{col} TEXT" for col in columns])  # Assuming all columns are of type TEXT
    create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {columns_with_types});"
    cursor.execute(create_table_sql)
    conn.commit()


def table_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone() is not None


def fetch_and_display_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    print(f"\nData in table '{table_name}':")
    for row in rows:
        print(row)
    print()  # Add a newline for better readability


def insert_or_update(conn, table_name, data):
    cursor = conn.cursor()
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?' for _ in data])

    # Check if the record exists
    select_sql = f"SELECT id FROM {table_name} WHERE id = ?"
    cursor.execute(select_sql, (data['id'],))
    result = cursor.fetchone()

    if result:
        # Update existing record (SCD Type 0: overwrite current values)
        update_columns = ', '.join([f'{col} = ?' for col in data.keys() if col != 'id'])
        update_sql = f"UPDATE {table_name} SET {update_columns} WHERE id = ?"
        cursor.execute(update_sql, (*[data[col] for col in data.keys() if col != 'id'], data['id']))
    else:
        # Insert new record
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(insert_sql, tuple(data.values()))

    conn.commit()


def main():
    db_file = 'scd_type0.db'
    conn = create_connection(db_file)

    # User input for table creation or update
    table_name = input("Enter the table name: ")

    columns = []  # Initialize columns variable

    if table_exists(conn, table_name):
        print(f"Table '{table_name}' already exists.")
        action = input("Do you want to (U)pdate existing records or (C)reate a new table? (U/C): ").strip().upper()
        if action == 'C':
            columns = input("Enter the column names separated by commas: ").split(',')
            columns = [col.strip() for col in columns]
            create_table(conn, table_name, columns)
        elif action == 'U':
            # If updating, we need to retrieve the existing columns
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [row[1] for row in cursor.fetchall()]  # Get column names from the existing table
            print(f"Existing columns: {columns}")
            print("You can now update existing records.")
    else:
        columns = input("Enter the column names separated by commas: ").split(',')
        columns = [col.strip() for col in columns]
        create_table(conn, table_name, columns)

    # Display current data before any updates
    fetch_and_display_data(conn, table_name)

    # User input for data insertion
    while True:
        data = {}
        for col in columns:
            value = input(f"Enter value for {col} (or type 'exit' to stop): ")
            if value.lower() == 'exit':
                conn.close()  # Close the connection before exiting
                return
            data[col] = value

        # Prompt for ID if not included in data
        if 'id' not in data:
            data['id'] = input("Enter the ID for this record: ")

        insert_or_update(conn, table_name, data)

        # Display current data after the update
        fetch_and_display_data(conn, table_name)


if __name__ == "__main__":
    main()
