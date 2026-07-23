#1 scd2

import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('scd_type2.db')
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
        is_current INTEGER,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
''')
# Function to insert a new customer
def insert_customer(customer_id, name, email, address, phone):
    cursor.execute('''
        INSERT INTO customers (customer_id, name, email, address, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, name, email, address, phone))
    conn.commit()

# Function to update a customer
def update_customer(customer_id, name, email, address, phone):
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

# Example usage
insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')
update_customer(1, 'Jane Doe', 'jane@example.com', '456 Elm St', '987-654-3210')

# Close the database connection
conn.close()


#2 scd1

import sqlite3

# Connect to the database
conn = sqlite3.connect('scd_type1.db')
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

# Function to insert a new customer
def insert_customer(customer_id, name, email, address, phone):
    cursor.execute('''
        INSERT INTO customers (customer_id, name, email, address, phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, name, email, address, phone))
    conn.commit()

# Function to update a customer
def update_customer(customer_id, name, email, address, phone):
    cursor.execute('''
        UPDATE customers
        SET name = ?, email = ?, address = ?, phone = ?
        WHERE customer_id = ?
    ''', (name, email, address, phone, customer_id))
    conn.commit()

# Example usage
insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')
update_customer(1, 'Jane Doe', 'jane@example.com', '456 Elm St', '987-654-3210')

# Close the database connection
conn.close()

#3 scd3

import sqlite3

# Connect to the database
conn = sqlite3.connect('scd_type3.db')
cursor = conn.cursor()

# Create the customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        current_name TEXT,
        previous_name TEXT,
        current_email TEXT,
        previous_email TEXT,
        current_address TEXT,
        previous_address TEXT,
        current_phone TEXT,
        previous_phone TEXT
    )
''')

# Function to insert a new customer
def insert_customer(customer_id, name, email, address, phone):
    cursor.execute('''
        INSERT INTO customers (customer_id, current_name, current_email, current_address, current_phone)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, name, email, address, phone))
    conn.commit()

# Function to update a customer
def update_customer(customer_id, name, email, address, phone):
    cursor.execute('''
        SELECT * FROM customers
        WHERE customer_id = ?
    ''', (customer_id,))
    current_record = cursor.fetchone()

    if current_record:
        cursor.execute('''
            UPDATE customers
            SET previous_name = ?, previous_email = ?, previous_address = ?, previous_phone = ?,
                current_name = ?, current_email = ?, current_address = ?, current_phone = ?
            WHERE customer_id = ?
        ''', (current_record[1], current_record[3], current_record[5], current_record[7],
              name, email, address, phone, customer_id))
        conn.commit()

# Example usage
insert_customer(1, 'John Doe', 'john@example.com', '123 Main St', '123-456-7890')
update_customer(1, 'Jane Doe', 'jane@example.com', '456 Elm St', '987-654-3210')

# Close the database connection
conn.close()


#4 scd4

import sqlite3

conn = sqlite3.connect('scd_type4.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_history (
        history_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        name TEXT,
        email TEXT,
        start_date DATE,
        end_date DATE
    )
''')

def update_customer(customer_id, name, email):
    cursor.execute('''
        UPDATE customer_history
        SET end_date = ?
        WHERE customer_id = ? AND end_date IS NULL
    ''', ('2022-01-01', customer_id))
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date)
        VALUES (?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01'))
    conn.commit()

update_customer(1, 'Jane Doe', 'jane@example.com')

#5 scd5

import sqlite3

conn = sqlite3.connect('scd_type5.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_history (
        history_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        name TEXT,
        email TEXT,
        start_date DATE,
        end_date DATE,
        reason TEXT
    )
''')

def update_customer(customer_id, name, email, reason):
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date, reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01', reason))
    conn.commit()

update_customer(1, 'Jane Doe', 'jane@example.com', 'Updated email address')


#6 scd6

import sqlite3

conn = sqlite3.connect('scd_type6.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_history (
        history_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        name TEXT,
        email TEXT,
        start_date DATE,
        end_date DATE,
        reason TEXT,
        updated_by TEXT
    )
''')

def update_customer(customer_id, name, email, reason, updated_by):
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date, reason, updated_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01', reason, updated_by))
    conn.commit()

update_customer(1, 'Jane Doe', 'jane@example.com', 'Updated email address', 'John Doe')

#7 

import sqlite3

# Connect to the database
conn = sqlite3.connect('scd_types.db')
cursor = conn.cursor()

# Create the customers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')

# Create the customer_history table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS customer_history (
        history_id INTEGER PRIMARY KEY,
        customer_id INTEGER,
        name TEXT,
        email TEXT,
        start_date DATE,
        end_date DATE,
        reason TEXT,
        updated_by TEXT
    )
''')

# SCD Type 1: Overwrite existing data with new values
def update_customer_scd1(customer_id, name, email):
    cursor.execute('''
        UPDATE customers
        SET name = ?, email = ?
        WHERE customer_id = ?
    ''', (name, email, customer_id))
    conn.commit()

# SCD Type 2: Store history of changes in a separate table
def update_customer_scd2(customer_id, name, email):
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date)
        VALUES (?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01'))
    conn.commit()

# SCD Type 3: Store current and previous values in the same table
def update_customer_scd3(customer_id, name, email):
    cursor.execute('''
        UPDATE customers
        SET previous_name = current_name, previous_email = current_email,
            current_name = ?, current_email = ?
        WHERE customer_id = ?
    ''', (name, email, customer_id))
    conn.commit()

# SCD Type 4: Store history of changes in a separate table with end date
def update_customer_scd4(customer_id, name, email):
    cursor.execute('''
        UPDATE customer_history
        SET end_date = ?
        WHERE customer_id = ? AND end_date IS NULL
    ''', ('2022-01-01', customer_id))
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date)
        VALUES (?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01'))
    conn.commit()

# SCD Type 5: Store history of changes in a separate table with reason
def update_customer_scd5(customer_id, name, email, reason):
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date, reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01', reason))
    conn.commit()

# SCD Type 6: Store history of changes in a separate table with reason and updated_by
def update_customer_scd6(customer_id, name, email, reason, updated_by):
    cursor.execute('''
        INSERT INTO customer_history (customer_id, name, email, start_date, reason, updated_by)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (customer_id, name, email, '2022-01-01', reason, updated_by))
    conn.commit()

# Test the functions
update_customer_scd1(1, 'Jane Doe', 'jane@example.com')
update_customer_scd2(1, 'Jane Doe', 'jane@example.com')
update_customer_scd3(1, 'Jane Doe', 'jane@example.com')
update_customer_scd4(1, 'Jane Doe', 'jane@example.com')
update_customer_scd5(1, 'Jane Doe', 'jane@example.com', 'Updated email address')
update_customer_scd6(1, 'Jane Doe', 'jane@example.com', 'Updated email address', 'John Doe')

# Close the database connection
conn.close()

