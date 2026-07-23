import sqlite3
# Type 3: Add new attributes for changes; limited history (current and previous).
# Connect to the database
conn = sqlite3.connect('scd_type_3.db')
cursor = conn.cursor()

# Create the customers table with current and previous values
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        current_name TEXT,
        previous_name TEXT,
        current_email TEXT,
        previous_email TEXT,
        current_address TEXT,
        previous_address TEXT,
        phone TEXT
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
            INSERT INTO customers (customer_id, current_name, current_email, current_address, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, name, email, address, phone))
        conn.commit()
        print(f"Inserted new customer with ID {customer_id}.")


# SCD Type 3: Update customer and store previous values
def update_customer_scd3(customer_id, name, email, address):
    cursor.execute('''
        SELECT * FROM customers WHERE customer_id = ?
    ''', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        # Update previous values with current values
        cursor.execute('''
            UPDATE customers
            SET previous_name = current_name,
                previous_email = current_email,
                previous_address = current_address,
                current_name = ?,
                current_email = ?,
                current_address = ?,
                phone = ?
            WHERE customer_id = ?
        ''', (name, email, address, existing_customer[7], customer_id))  # Use existing phone number
        print(f"Updated customer with ID {customer_id}.")
    else:
        print(f"Customer with ID {customer_id} does not exist. Cannot update.")


# Example Usage
try:
    # Insert a new customer
    insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')

    # Update the customer (SCD Type 3)
    update_customer_scd3(1, 'John Doe Updated', 'john.updated@example.com', '123 Main St')

    # Attempt to insert a customer with the same ID (this will show a message instead of causing an error)
    insert_customer(1, 'Jane Doe', 'jane@example.com', '789 Oak St', '987-654-3210')

    # Update the customer again (SCD Type 3)
    update_customer_scd3(1, 'John Smith', 'john.smith@example.com', '456 Elm St')

    # Display current customer data
    cursor.execute('SELECT * FROM customers')
    current_customers = cursor.fetchall()
    print("Current Customers:")
    for customer in current_customers:
        print(customer)

except sqlite3.Error as e:
    print(f"SQLite error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    # Close the database connection
    if conn:
        conn.close()
