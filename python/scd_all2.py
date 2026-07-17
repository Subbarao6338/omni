import sqlite3
from datetime import datetime

# Connect to the database
def get_db_connection():
    return sqlite3.connect('scd.db')

# Define date format
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# Function to create a main table and its corresponding history table dynamically
def create_table_with_history(main_table_name, columns, previous_columns):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Create the main table
            columns_definition = ', '.join([f"{col} TEXT" for col in columns + previous_columns])
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {main_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {columns_definition}
                )
            ''')

            # Create the history table
            history_table_name = f"{main_table_name}_history"
            history_columns_definition = ', '.join([f"{col} TEXT" for col in columns])
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {history_table_name} (
                    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id INTEGER,
                    {history_columns_definition},
                    start_date DATETIME,
                    end_date DATETIME,
                    reason TEXT,
                    updated_by TEXT,
                    FOREIGN KEY (id) REFERENCES {main_table_name} (id)
                )
            ''')
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while creating tables: {e}")

# Function to insert a new record into the main table
def insert_record(main_table_name, record):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            placeholders = ', '.join(['?'] * len(record))
            cursor.execute(f'''
                INSERT INTO {main_table_name} ({', '.join(record.keys())})
                VALUES ({placeholders})
            ''', tuple(record.values()))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while inserting record: {e}")

# Function to check if a record exists
def record_exists(main_table_name, record_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f'SELECT 1 FROM {main_table_name} WHERE id = ?', (record_id,))
        return cursor.fetchone() is not None

# SCD Type 1: Overwrite existing data with new values
def update_record_scd1(main_table_name, record_id, updates):
    if not record_exists(main_table_name, record_id):
        print(f"Record with ID {record_id} does not exist.")
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
            cursor.execute(f'''
                UPDATE {main_table_name}
                SET {set_clause}
                WHERE id = ?
            ''', (*updates.values(), record_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating record: {e}")

# SCD Type 2: Store history of changes in a separate table
def update_record_scd2(main_table_name, record_id, updates):
    if not record_exists(main_table_name, record_id):
        print(f"Record with ID {record_id} does not exist.")
        return

    history_table_name = f"{main_table_name}_history"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Get the current record from the history table
            cursor.execute(f'''
                SELECT * FROM {history_table_name}
                WHERE id = ? AND end_date IS NULL
            ''', (record_id,))
            current_record = cursor.fetchone()

            # If a current record exists, update its end date to the current timestamp
            if current_record:
                end_date = datetime.now().strftime(DATE_FORMAT)
                cursor.execute(f'''
                    UPDATE {history_table_name}
                    SET end_date = ?
                    WHERE history_id = ?
                ''', (end_date, current_record[0]))

            # Insert a new record with the updated values
            start_date = datetime.now().strftime(DATE_FORMAT)
            cursor.execute(f'''
                INSERT INTO {history_table_name} (id, {', '.join(updates.keys())}, start_date, end_date)
                VALUES (?, {', '.join(['?'] * len(updates))}, ?, NULL)
            ''', (record_id, *updates.values(), start_date))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating record SCD Type 2: {e}")

# SCD Type 3: Store current and previous values in the same table
def update_record_scd3(main_table_name, record_id, updates, previous_columns):
    if not record_exists(main_table_name, record_id):
        print(f"Record with ID {record_id} does not exist.")
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            set_clause = ', '.join([f"{prev} = {prev}, {curr} = ?" for prev, curr in zip(previous_columns, updates.keys())])
            cursor.execute(f'''
                UPDATE {main_table_name}
                SET {set_clause}
                WHERE id = ?
            ''', (*updates.values(), record_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating record SCD Type 3: {e}")

# SCD Type 4: Store history of changes in a separate table with end date
def update_record_scd4(main_table_name, record_id, updates):
    if not record_exists(main_table_name, record_id):
        print(f"Record with ID {record_id} does not exist.")
        return

    history_table_name = f"{main_table_name}_history"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Update the end date of the current record
            cursor.execute(f'''
                UPDATE {history_table_name}
                SET end_date = ?
                WHERE id = ? AND end_date IS NULL
            ''', (datetime.now().strftime(DATE_FORMAT), record_id))

            # Insert a new record with the updated values
            start_date = datetime.now().strftime(DATE_FORMAT)
            cursor.execute(f'''
                INSERT INTO {history_table_name} (id, {', '.join(updates.keys())}, start_date, end_date)
                VALUES (?, {', '.join(['?'] * len(updates))}, ?, NULL)
            ''', (record_id, *updates.values(), start_date))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating record SCD Type 4: {e}")

# SCD Type 5: Store history of changes in a separate table with reason
def update_record_scd5(main_table_name, record_id, updates, reason):
    if not record_exists(main_table_name, record_id):
        print(f"Record with ID {record_id} does not exist.")
        return

    history_table_name = f"{main_table_name}_history"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Update the end date of the current record
            cursor.execute(f'''
                UPDATE {history_table_name}
                SET end_date = ?
                WHERE id = ? AND end_date IS NULL
            ''', (datetime.now().strftime(DATE_FORMAT), record_id))

            # Insert a new record with the updated values and reason
            start_date = datetime.now().strftime(DATE_FORMAT)
            cursor.execute(f'''
                INSERT INTO {history_table_name} (id, {', '.join(updates.keys())}, start_date, end_date, reason)
                VALUES (?, {', '.join(['?'] * len(updates))}, ?, NULL, ?)
            ''', (record_id, *updates.values(), start_date, reason))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating record SCD Type 5: {e}")

# SCD Type 6: Store history of changes in a separate table with reason and updated_by
def update_record_scd6(main_table_name, record_id, updates, reason, updated_by):
    if not record_exists(main_table_name, record_id):
        print(f"Record with ID {record_id} does not exist.")
        return

    history_table_name = f"{main_table_name}_history"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            # Update the end date of the current record
            cursor.execute(f'''
                UPDATE {history_table_name}
                SET end_date = ?
                WHERE id = ? AND end_date IS NULL
            ''', (datetime.now().strftime(DATE_FORMAT), record_id))

            # Insert a new record with the updated values, reason, and updated_by
            start_date = datetime.now().strftime(DATE_FORMAT)
            cursor.execute(f'''
                INSERT INTO {history_table_name} (id, {', '.join(updates.keys())}, start_date, end_date, reason, updated_by)
                VALUES (?, {', '.join(['?'] * len(updates))}, ?, NULL, ?, ?)
            ''', (record_id, *updates.values(), start_date, reason, updated_by))
            conn.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while updating record SCD Type 6: {e}")

# Example usage
if __name__ == "__main__":
    # ###1 Dynamic
    # # Dynamic input for table name and columns
    # main_table_name = input("Enter the main table name: ")
    # columns = input("Enter the columns (comma-separated): ").split(',')
    # previous_columns = input("Enter the previous columns (comma-separated): ").split(',')
    #
    # # Strip whitespace from column names
    # columns = [col.strip() for col in columns]
    # previous_columns = [col.strip() for col in previous_columns]
    #
    # # Create the main table and its history table
    # create_table_with_history(main_table_name, columns, previous_columns)
    #
    # # Example record insertion
    # record = {col: f"{col}_value" for col in columns}
    # insert_record(main_table_name, record)

    ###1 Static
    main_table_name = 'customers'
    columns = ['name', 'email', 'address', 'phone']
    previous_columns = ['previous_name', 'previous_email', 'previous_address', 'previous_phone']

    # Create the main table and its history table
    create_table_with_history(main_table_name, columns, previous_columns)

    # Insert a new record
    insert_record(main_table_name, {
        'name': 'John Doe',
        'email': 'john@example.com',
        'address': '123 Main St',
        'phone': '123-456-7890'
    })

    # Update record using SCD Type 1
    update_record_scd1(main_table_name, 1, {
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'address': '456 Elm St',
        'phone': '987-654-3210'
    })

    # Update record using SCD Type 2
    update_record_scd2(main_table_name, 1, {
        'name': 'Jane Doe',
        'email': 'jane@example.com',
        'address': '456 Elm St',
        'phone': '987-654-3210'
    })

    # Update record using SCD Type 3
    update_record_scd3(main_table_name, 1, {
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'address': '789 Oak St',
        'phone': '555-555-5555'
    }, previous_columns)

    # Update record using SCD Type 4
    update_record_scd4(main_table_name, 1, {
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'address': '789 Oak St',
        'phone': '555-555-5555'
    })

    # Update record using SCD Type 5
    update_record_scd5(main_table_name, 1, {
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'address': '789 Oak St',
        'phone': '555-555-5555'
    }, 'Updated contact information')

    # Update record using SCD Type 6
    update_record_scd6(main_table_name, 1, {
        'name': 'Jane Smith',
        'email': 'jane.smith@example.com',
        'address': '789 Oak St',
        'phone': '555-555-5555'
    }, 'Updated contact information', 'Admin')

    print("Database operations completed successfully.")
