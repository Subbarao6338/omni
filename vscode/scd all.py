import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('scd_types.db')
cursor = conn.cursor()

# Function to create a main table and a history table dynamically
def create_tables(main_table_name, history_table_name, columns):
    # Create the main table
    columns_definition = ', '.join([f"{col} TEXT" for col in columns])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {main_table_name} (
            id INTEGER PRIMARY KEY,
            {columns_definition}
        )
    ''')

    # Create the history table
    history_columns_definition = ', '.join([f"{col} TEXT" for col in columns])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {history_table_name} (
            history_id INTEGER PRIMARY KEY,
            id INTEGER,
            {history_columns_definition},
            start_date DATE,
            end_date DATE,
            is_current INTEGER,
            FOREIGN KEY (id) REFERENCES {main_table_name} (id)
        )
    ''')
    conn.commit()

# Function to insert a new record into the main table
def insert_record(main_table_name, record):
    placeholders = ', '.join(['?'] * len(record))
    cursor.execute(f'''
        INSERT INTO {main_table_name} ({', '.join(record.keys())})
        VALUES ({placeholders})
    ''', tuple(record.values()))
    conn.commit()

# SCD Type 1: Overwrite existing data with new values
def update_record_scd1(main_table_name, record_id, updates):
    set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
    cursor.execute(f'''
        UPDATE {main_table_name}
        SET {set_clause}
        WHERE id = ?
    ''', (*updates.values(), record_id))
    conn.commit()

# SCD Type 2: Store history of changes in a separate table
def update_record_scd2(main_table_name, history_table_name, record_id, updates):
    # Get the current record
    cursor.execute(f'''
        SELECT * FROM {history_table_name}
        WHERE id = ? AND is_current = 1
    ''', (record_id,))
    current_record = cursor.fetchone()

    # If a current record exists, update its end date
    if current_record:
        cursor.execute(f'''
            UPDATE {history_table_name}
            SET end_date = ?
            WHERE history_id = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), current_record[0]))

    # Insert a new record with the updated values
    start_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(f'''
        INSERT INTO {history_table_name} (id, {', '.join(updates.keys())}, start_date, is_current)
        VALUES (?, {', '.join(['?'] * len(updates))}, ?, 1)
    ''', (record_id, *updates.values(), start_date))
    conn.commit()

# SCD Type 3: Store current and previous values in the same table
def update_record_scd3(main_table_name, record_id, updates, previous_columns):
    set_clause = ', '.join([f"{prev} = {curr}" for prev, curr in zip(previous_columns, updates.keys())])
    cursor.execute(f'''
        UPDATE {main_table_name}
        SET {set_clause}, {', '.join([f"{key} = ?" for key in updates.keys()])}
        WHERE id = ?
    ''', (*updates.values(), record_id))
    conn.commit()

# Example usage
main_table_name = 'customers'
history_table_name = 'customer_history'
columns = ['name', 'email', 'address', 'phone']

# Create tables
create_tables(main_table_name, history_table_name, columns)

# Insert a new record
insert_record(main_table_name, {'name': 'John Doe', 'email': 'john@example.com', 'address': '123 Main St', 'phone': '123-456-7890'})

# Update record using SCD Type 1
update_record_scd1(main_table_name, 1, {'name': 'Jane Doe', 'email': 'jane@example.com', 'address': '456 Elm St', 'phone': '987-654-3210'})

# Update record using SCD Type 2
update_record_scd2(main_table_name, history_table_name, 1, {'name': 'Jane Doe', 'email': 'jane@example.com', 'address': '456 Elm St', 'phone': '987-654-3210'})

# Update record using SCD Type 3
# SCD Type 3: Store current and previous values in the same table
def update_record_scd3(main_table_name, record_id, updates, previous_columns):
    # Prepare the SQL statement to update previous values and current values
    set_clause = ', '.join([f"{prev} = {prev}, {curr} = ?" for prev, curr in zip(previous_columns, updates.keys())])
    cursor.execute(f'''
        UPDATE {main_table_name}
        SET {set_clause}
        WHERE id = ?
    ''', (*updates.values(), record_id))
    conn.commit()

# Example usage
main_table_name = 'customers'
history_table_name = 'customer_history'
columns = ['name', 'email', 'address', 'phone']
previous_columns = ['previous_name', 'previous_email', 'previous_address', 'previous_phone']

# Create tables
create_tables(main_table_name, history_table_name, columns)

# Insert a new record
insert_record(main_table_name, {'name': 'John Doe', 'email': 'john@example.com', 'address': '123 Main St', 'phone': '123-456-7890'})

# Update record using SCD Type 1
update_record_scd1(main_table_name, 1, {'name': 'Jane Doe', 'email': 'jane@example.com', 'address': '456 Elm St', 'phone': '987-654-3210'})

# Update record using SCD Type 2
update_record_scd2(main_table_name, history_table_name, 1, {'name': 'Jane Doe', 'email': 'jane@example.com', 'address': '456 Elm St', 'phone': '987-654-3210'})

# Update record using SCD Type 3
update_record_scd3(main_table_name, 1, {'name': 'Jane Smith', 'email': 'jane.smith@example.com', 'address': '789 Oak St', 'phone': '555-555-5555'}, previous_columns)

# Close the database connection
conn.close()
