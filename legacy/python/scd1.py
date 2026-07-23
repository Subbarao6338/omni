import sqlite3
# Type 1: Overwrite existing data; no history.
# Connect to the database
conn = sqlite3.connect('scd_type_1.db')
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


# Function to insert or update a customer (SCD Type 1)
def upsert_customer(customer_id, name, email, address, phone):
    # Check if the customer already exists
    cursor.execute('''
        SELECT * FROM customers WHERE customer_id = ?
    ''', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        # Update the existing customer record
        cursor.execute('''
            UPDATE customers
            SET name = ?, email = ?, address = ?, phone = ?
            WHERE customer_id = ?
        ''', (name, email, address, phone, customer_id))
        print(f"Updated customer with ID {customer_id}.")
    else:
        # Insert a new customer record
        cursor.execute('''
            INSERT INTO customers (customer_id, name, email, address, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, name, email, address, phone))
        print(f"Inserted customer with ID {customer_id}.")

    conn.commit()


try:
    # Insert new customers
    upsert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')
    upsert_customer(2, 'Jane Smith', 'jane@example.com', '456 Elm St', '987-654-3210')

    # Update an existing customer
    upsert_customer(1, 'John Doe Updated', 'john.updated@example.com', '123 Main St', '123-456-7890')

    # Display all customers
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    print("Current Customers:")
    for customer in customers:
        print(customer)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the database connection
    conn.close()
