import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('scd_type_2.db')
cursor = conn.cursor()


# Function to create a table and its history table
def create_table_with_history(table_name, columns):
    # Create the main table
    column_definitions = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY,
            {column_definitions}
        )
    ''')

    # Create the history table
    history_table_name = f"{table_name}_history"
    history_columns = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns.items()])
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {history_table_name} (
            history_id INTEGER PRIMARY KEY,
            id INTEGER,
            {history_columns},
            start_date DATETIME,
            end_date DATETIME,
            FOREIGN KEY (id) REFERENCES {table_name} (id)
        )
    ''')
    conn.commit()


# Function to check if a table exists
def table_exists(table_name):
    cursor.execute(f'''
        SELECT name FROM sqlite_master WHERE type='table' AND name=?
    ''', (table_name,))
    return cursor.fetchone() is not None


# Function to get columns of a table
def get_table_columns(table_name):
    cursor.execute(f'PRAGMA table_info({table_name})')
    return {row[1]: row[2] for row in cursor.fetchall()}  # {column_name: column_type}


# Function to insert a new record
def insert_record(table_name, record):
    cursor.execute(f'''
        INSERT INTO {table_name} ({', '.join(record.keys())})
        VALUES ({', '.join(['?' for _ in record])})
    ''', tuple(record.values()))
    conn.commit()
    print(f"Inserted new record into {table_name}.")


# SCD Type 2: Update record and store history
def update_record_scd2(table_name, record_id, updated_record):
    history_table_name = f"{table_name}_history"

    # Get the current record from the history table
    cursor.execute(f'''
        SELECT * FROM {history_table_name}
        WHERE id = ? AND end_date IS NULL
    ''', (record_id,))
    current_record = cursor.fetchone()

    # If a current record exists, update its end date to today
    if current_record:
        end_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(f'''
            UPDATE {history_table_name}
            SET end_date = ?
            WHERE history_id = ?
        ''', (end_date, current_record[0]))

    # Insert a new record into the history table with updated values
    updated_record['id'] = record_id  # Ensure the ID is set for the new history record
    cursor.execute(f'''
        INSERT INTO {history_table_name} (id, {', '.join(updated_record.keys())}, start_date, end_date)
        VALUES (?, {', '.join(['?' for _ in updated_record])}, ?, NULL)
    ''', (record_id, *updated_record.values(), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    # Update the main table with the latest information
    cursor.execute(f'''
        UPDATE {table_name}
        SET {', '.join([f"{key} = ?" for key in updated_record.keys()])}
        WHERE id = ?
    ''', (*updated_record.values(), record_id))

    conn.commit()

# Function to display current records
def display_current_records(table_name):
    cursor.execute(f'SELECT * FROM {table_name}')
    current_records = cursor.fetchall()
    print(f"\nCurrent Records in {table_name}:")
    for record in current_records:
        print(record)
# Main function to run the program
def main():
    try:
        # Get table name from user
        table_name = input("Enter the table name: ").strip()

        # Check if the table exists
        if not table_exists(table_name):
            columns_input = input("Table does not exist. Enter the columns (name:type, email:type, ...): ").strip()

            # Validate and parse columns
            columns = {}
            for col in columns_input.split(','):
                try:
                    col_name, col_type = col.split(':')
                    col_name = col_name.strip()
                    col_type = col_type.strip()
                    if not col_name or not col_type:
                        raise ValueError("Column name and type cannot be empty.")
                    columns[col_name] = col_type
                except ValueError as e:
                    print(f"Invalid column format: {col}. Expected format is name:type. Error: {e}")
                    return

            # Create the table and its history table
            create_table_with_history(table_name, columns)
            print(f"Table '{table_name}' created successfully.")
        else:
            print(f"Table '{table_name}' already exists.")
            # Get the columns of the existing table
            columns = get_table_columns(table_name)
        # Display current records before any action
        display_current_records(table_name)
        # Prompt for record insertion or update
        action = input("Do you want to (I)nsert a new record or (U)pdate an existing record? (I/U): ").strip().upper()

        if action == 'I':
            # Insert a new record
            record_input = input(f"Enter a new record for {table_name} ({', '.join(columns.keys())}): ").strip()
            record_values = record_input.split(',')

            if len(record_values) != len(columns):
                print(f"Expected {len(columns)} values, but got {len(record_values)}.")
                return

            record = {list(columns.keys())[i]: record_values[i].strip() for i in range(len(columns))}
            insert_record(table_name, record)

        elif action == 'U':
            # Update the record (SCD Type 2)
            record_id = input("Enter the ID of the record to update: ").strip()
            if not record_id.isdigit():
                print("Record ID must be a number.")
                return

            record_id = int(record_id)

            # Provide clear instructions for the expected input
            print(f"Enter updated record values for {table_name} ({', '.join(columns.keys())}):")
            updated_record_input = input().strip()
            updated_record_values = updated_record_input.split(',')

            # Check if the number of provided values matches the number of columns
            if len(updated_record_values) != len(columns):
                print(f"Expected {len(columns)} values, but got {len(updated_record_values)}.")
                print(f"Please provide values in the format: {', '.join(columns.keys())}")
                return

            updated_record = {list(columns.keys())[i]: updated_record_values[i].strip() for i in range(len(columns))}

            # Validate that the record exists before updating
            cursor.execute(f'''
                SELECT * FROM {table_name} WHERE id = ?
            ''', (record_id,))
            if cursor.fetchone() is None:
                print(f"No record found with ID {record_id}.")
                return

            # Call the function to update the record using SCD Type 2 logic
            update_record_scd2(table_name, record_id, updated_record)

        else:
            print("Invalid action. Please enter 'I' to insert or 'U' to update.")
            return

        # Display current records after the action
        display_current_records(table_name)

        # Display history records
        history_table_name = f"{table_name}_history"
        if table_exists(history_table_name):
            display_current_records(history_table_name)
        else:
            print(f"No history table found for {table_name}.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()


# Run the main function
if __name__ == "__main__":
    main()
