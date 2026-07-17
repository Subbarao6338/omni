import sqlite3
from datetime import datetime
# Type 4: Use a separate historical table; current data in one table, history in another.
# Connect to the database
conn = sqlite3.connect('scd_type_4.db')
cursor = conn.cursor()

# Create the customers table for current data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        address TEXT,
        phone TEXT
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
        start_date DATE,
        end_date DATE,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
''')

# Function to insert a new customer
def insert_customer(name, email, address, phone):
    # Check if the customer already exists
    cursor.execute('''
        SELECT * FROM customers WHERE email = ?
    ''', (email,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        print(f"Customer with email {email} already exists.")
    else:
        cursor.execute('''
            INSERT INTO customers (name, email, address, phone)
            VALUES (?, ?, ?, ?)
        ''', (name, email, address, phone))
        conn.commit()


# SCD Type 4: Update customer and store history
def update_customer_scd4(customer_id, name, email, address, phone):
    # Get the current record from the customers table
    cursor.execute('''
        SELECT * FROM customers WHERE customer_id = ?
    ''', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        # Update the end date of the existing history record
        cursor.execute('''
            UPDATE customer_history
            SET end_date = ?
            WHERE customer_id = ? AND end_date IS NULL
        ''', (datetime.now().strftime('%Y-%m-%d'), customer_id))

        # Insert the current record into customer_history
        cursor.execute('''
            INSERT INTO customer_history (customer_id, name, email, address, phone, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?, NULL)
        ''', (customer_id, existing_customer[1], existing_customer[2], existing_customer[3], existing_customer[4],
              datetime.now().strftime('%Y-%m-%d')))

        # Update the customers table with the new values
        cursor.execute('''
            UPDATE customers
            SET name = ?, email = ?, address = ?, phone = ?
            WHERE customer_id = ?
        ''', (name, email, address, phone, customer_id))

        print(f"Updated customer with ID {customer_id}.")
    else:
        print(f"Customer with ID {customer_id} does not exist.")

    conn.commit()

# Example Usage
try:
    # Insert a new customer
    insert_customer('John Doe', 'john@example.com', '123 Main St', '123-456-7890')

    # Update the customer (SCD Type 4)
    update_customer_scd4(1, 'John Doe Updated', 'john.updated@example.com', '123 Main St', '123-456-7890')

    # Update the customer again (SCD Type 4)
    update_customer_scd4(1, 'John Smith', 'john.smith@example.com', '456 Elm St', '987-654-3210')

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
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close
