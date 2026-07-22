import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('scd_type_2.db')
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

# Create the customer_history table
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
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
''')


# Function to insert a new customer
def insert_customer(customer_id, name, email, address, phone):
    # Check if the customer_id already exists
    cursor.execute('''
        SELECT * FROM customers WHERE customer_id = ?
    ''', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        print(f"Customer with ID {customer_id} already exists. Use update instead.")
    else:
        cursor.execute('''
            INSERT INTO customers (customer_id, name, email, address, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, name, email, address, phone))
        conn.commit()
        print(f"Inserted new customer with ID {customer_id}.")


# SCD Type 2: Update customer and store history
def update_customer_scd2(customer_id, name, email, address, phone):
    # Get the current record from customer_history
    cursor.execute('''
        SELECT * FROM customer_history
        WHERE customer_id = ? AND end_date IS NULL
    ''', (customer_id,))
    current_record = cursor.fetchone()

    # If a current record exists, update its end date to today
    if current_record:
        end_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            UPDATE customer_history
            SET end_date = ?
            WHERE history_id = ?
        ''', (end_date, current_record[0]))
    else:
        print(f"No current record found for customer ID {customer_id}. Creating a new history record.")

    # Insert a new record into customer_history
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, address, phone, start_date, end_date)
        VALUES (?, ?, ?, ?, ?, ?, NULL)
    ''', (customer_id, name, email, address, phone, datetime.now().strftime('%Y-%m-%d')))

    # Update the customers table with the latest information
    cursor.execute('''
        UPDATE customers
        SET name = ?, email = ?, address = ?, phone = ?
        WHERE customer_id = ?
    ''', (name, email, address, phone, customer_id))

    conn.commit()


# Example Usage
try:
    # Insert a new customer
    insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')

    # Update the customer (SCD Type 2)
    update_customer_scd2(1, 'John Doe Updated', 'john.updated@example.com', '123 Main St', '123-456-7890')

    # Update the customer again (SCD Type 2)
    update_customer_scd2(1, 'John Smith', 'john.smith@example.com', '456 Elm St', '987-654-3210')

    # Display current customer data
    cursor.execute('SELECT * FROM customers')
    current_customers = cursor.fetchall()
    print("Current Customers:")
    for customer in current_customers:
        print(customer)

    # Display customer history
    cursor.execute('SELECT * FROM customer_history')
    history_records = cursor.fetchall()
    print("\nCustomer History:")
    for record in history_records:
        print(record)

except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the database connection
    conn.close()
