import sqlite3

# Type 0: No changes; data remains static.

# Connect to the database
conn = sqlite3.connect('scd_type_0.db')
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


# Function to insert a new customer (SCD Type 0)
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
        print(f"Inserted customer with ID {customer_id}.")


try:
    # Insert new customers
    insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')
    insert_customer(2, 'Jane Smith', 'jane@example.com', '456 Elm St', '987-654-3210')

    # Attempt to insert a customer with an existing ID (should be skipped)
    insert_customer(1, 'John Doe Updated', 'john.updated@example.com', '123 Main St', '123-456-7890')

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
