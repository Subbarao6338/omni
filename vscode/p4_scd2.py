import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('scd_types_2.db')
cursor = conn.cursor()

# Create the customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT,
        address TEXT,
        phone TEXT
    )
''')

# Create the customer_history table with additional columns
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_history (
        history_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        name TEXT,
        email TEXT,
        address TEXT,
        phone TEXT,
        start_date DATE,
        end_date DATE,
        is_current INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
''')

# Function to insert a new customer
def insert_customer(customer_id, name, email, address, phone):
    # Check if the customer already exists
    cursor.execute('''
        SELECT * FROM customers WHERE customer_id = ?
    ''', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        print(f"Customer with ID {customer_id} already exists. Skipping insertion.")
    else:
        cursor.execute('''
            INSERT INTO customers (customer_id, name, email, address, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, name, email, address, phone))
        conn.commit()

# SCD Type 2: Store history of changes in a separate table
def update_customer_scd2(customer_id, name, email, address, phone):
    # Get the current record
    cursor.execute('''
        SELECT * FROM customer_history
        WHERE customer_id = ? AND is_current = 1
    ''', (customer_id,))
    current_record = cursor.fetchone()

    # If a current record exists, update its end date
    if current_record:
        cursor.execute('''
            UPDATE customer_history
            SET end_date = ?
            WHERE history_id = ?
        ''', (datetime.now().strftime('%Y-%m-%d'), current_record[0]))

    # Insert a new record with the updated values
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, address, phone, start_date, is_current)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    ''', (customer_id, name, email, address, phone, datetime.now().strftime('%Y-%m-%d')))
    conn.commit()

try:
    insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')
    update_customer_scd2(1, 'Jane Doe', 'jane@example.com', '456 Elm St', '987-654-3210')
    update_customer_scd2(1, 'Jane Smith', 'jane.smith@example.com', '789 Oak St', '555-555-5555')
    print("Updated Successfully")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close()
