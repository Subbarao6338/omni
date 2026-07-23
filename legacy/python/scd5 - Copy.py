import sqlite3
from datetime import datetime
# Type 5: Hybrid approach; combines features of multiple types 1,2,3.
# Connect to the database
conn = sqlite3.connect('scd_type_5.db')
cursor = conn.cursor()

# Create the current_customers table for current and previous values
cursor.execute('''
    CREATE TABLE IF NOT EXISTS current_customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        address TEXT,
        phone TEXT,
        previous_name TEXT,
        previous_email TEXT,
        previous_address TEXT,
        previous_phone TEXT
    )
''')

# Create the customer_history table for historical data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        name TEXT,
        email TEXT,
        address TEXT,
        phone TEXT,
        change_date DATE,
        FOREIGN KEY (customer_id) REFERENCES current_customers (customer_id)
    )
''')

# Function to insert a new customer
def insert_customer(name, email, address, phone):
    cursor.execute('''
        INSERT INTO current_customers (name, email, address, phone)
        VALUES (?, ?, ?, ?)
    ''', (name, email, address, phone))
    conn.commit()

# SCD Type 5: Update customer and store history
def update_customer_scd5(customer_id, name, email, address, phone):
    # Get the current record from the current_customers table
    cursor.execute('''
        SELECT * FROM current_customers WHERE customer_id = ?
    ''', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        # Insert the current record into customer_history
        cursor.execute('''
            INSERT INTO customer_history (customer_id, name, email, address, phone, change_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_id, existing_customer[1], existing_customer[2], existing_customer[3], existing_customer[4],
              datetime.now().strftime('%Y-%m-%d')))

        # Update the current_customers table with the new values
        cursor.execute('''
            UPDATE current_customers
            SET previous_name = ?, previous_email = ?, previous_address = ?, previous_phone = ?,
                name = ?, email = ?, address = ?, phone = ?
            WHERE customer_id = ?
        ''', (existing_customer[1], existing_customer[2], existing_customer[3], existing_customer[4],
              name, email, address, phone, customer_id))

        print(f"Updated customer with ID {customer_id}.")
    else:
        print(f"Customer with ID {customer_id} does not exist.")

    conn.commit()

# Example Usage
try:
    # Insert a new customer
    insert_customer('John Doe', 'john@example.com', '123 Main St', '123-456-7890')

    # Update the customer (SCD Type 5)
    update_customer_scd5(1, 'John Doe Updated', 'john.updated@example.com', '123 Main St', '123-456-7890')

    # Update the customer again (SCD Type 5)
    update_customer_scd5(1, 'John Smith', 'john.smith@example.com', '456 Elm St', '987-654-3210')

    # Display current customer data
    cursor.execute('SELECT * FROM current_customers')
    current_customers = cursor.fetchall()
    print("Current Customers (SCD Type 5):")
    for customer in current_customers:
        print(customer)

    # Display customer history
    cursor.execute('SELECT * FROM customer_history')
    history_records = cursor.fetchall()
    print("\nCustomer History (SCD Type 5):")
    for record in history_records:
        print(record)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close()
