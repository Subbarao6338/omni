import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('scd_type_6.db')
cursor = conn.cursor()

# Step 1: Create the customer dimension table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customer_dimension (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    customer_email TEXT,
    customer_address TEXT,
    current_value TEXT,
    previous_value TEXT,
    start_date TEXT,
    end_date TEXT
)
''')

# Step 2: Insert initial data only if the table is empty
cursor.execute('SELECT COUNT(*) FROM customer_dimension')
if cursor.fetchone()[0] == 0:
    initial_data = [
        (1, 'Alice', 'alice@example.com', '123 Main St', 'Active', None, '2021-01-01', None),
        (2, 'Bob', 'bob@example.com', '456 Elm St', 'Active', None, '2021-01-01', None),
        (3, 'Charlie', 'charlie@example.com', '789 Oak St', 'Active', None, '2021-01-01', None)
    ]
    cursor.executemany('''
    INSERT INTO customer_dimension (customer_id, customer_name, customer_email, customer_address, current_value, previous_value, start_date, end_date)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', initial_data)

# Commit the initial data
conn.commit()

# Step 3: New incoming customer data
new_customers = [
    (1, 'Alice Smith', 'alice.smith@example.com', '123 Main St', '2023-01-01'),
    (2, 'Bob', 'bob@example.com', '456 Elm St', '2023-01-01'),
    (3, 'Charlie Brown', 'charlie.brown@example.com', '789 Oak St', '2023-01-01')
]

# Debugging: Print existing records
cursor.execute('SELECT * FROM customer_dimension')
existing_records = cursor.fetchall()
print("Existing records in customer_dimension:")
for record in existing_records:
    print(record)

# Debugging: Print new customers to be processed
print("New customers to be processed:")
for customer in new_customers:
    print(customer)

# Step 4: Update the customer dimension table
for new_customer in new_customers:
    customer_id, customer_name, customer_email, customer_address, effective_date = new_customer

    # Check for existing customer
    cursor.execute('SELECT * FROM customer_dimension WHERE customer_id = ?', (customer_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        # Check for changes in customer attributes
        changes_detected = False
        previous_values = {}

        if existing_customer[1] != customer_name:
            previous_values['customer_name'] = existing_customer[1]
            changes_detected = True

        if existing_customer[2] != customer_email:
            previous_values['customer_email'] = existing_customer[2]
            changes_detected = True

        if existing_customer[3] != customer_address:
            previous_values['customer_address'] = existing_customer[3]
            changes_detected = True

        if changes_detected:
            # Update the end date of the existing record
            cursor.execute('''
            UPDATE customer_dimension
            SET end_date = ?, previous_value = ?
            WHERE customer_id = ?
            ''', (effective_date, str(previous_values), customer_id))

            # Insert a new record for the updated customer
            try:
                cursor.execute('''
                INSERT INTO customer_dimension (customer_id, customer_name, customer_email, customer_address, current_value, previous_value, start_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (customer_id, customer_name, customer_email, customer_address, 'Active', None, effective_date, None))
            except Exception as e:
                print(f"Error inserting customer_id {customer_id}: {e}")
    else:
        # If the record doesn't exist, add it as a new record
        try:
            cursor.execute('''
            INSERT INTO customer_dimension (customer_id, customer_name, customer_email, customer_address, current_value, previous_value, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (customer_id, customer_name, customer_email, customer_address, 'Active', None, effective_date, None))
        except Exception as e:
            print(f"Error inserting customer_id {customer_id}: {e}")

# Commit the changes
conn.commit()

# Step 5: Query the updated customer dimension table
cursor.execute('SELECT * FROM customer_dimension')
rows = cursor.fetchall()

# Display the updated customer dimension table
print("Updated customer dimension table:")
for row in rows:
    print(row)

# Close the connection
conn.close()

