import sqlite3
from faker import Faker
import random

# Initialize Faker for realistic data
fake = Faker()

# Database connection
conn = sqlite3.connect("DB PROJECT.db")
cursor = conn.cursor()

# Create Tables
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS employee (
                        eid INTEGER PRIMARY KEY AUTOINCREMENT,
                        ename TEXT NOT NULL,
                        email TEXT UNIQUE,
                        gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')),
                        contact TEXT,
                        dob DATE,
                        doj DATE,
                        pass TEXT,
                        utype TEXT CHECK(utype IN ('Admin', 'Employee')),
                        address TEXT,
                        salary REAL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS supplier (
                        invoice INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        contact TEXT,
                        desc TEXT
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS category (
                        cid INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                        pid INTEGER PRIMARY KEY AUTOINCREMENT,
                        category TEXT NOT NULL,
                        supplier TEXT NOT NULL,
                        name TEXT NOT NULL,
                        price REAL,
                        quantity INTEGER,
                        status TEXT CHECK(status IN ('Active', 'Inactive')),
                        FOREIGN KEY(category) REFERENCES category(name),
                        FOREIGN KEY(supplier) REFERENCES supplier(name)
                    )''')

    conn.commit()

# Generate Random Data for Employee Table
def generate_employee_data(n=100):
    genders = ['Male', 'Female', 'Other']
    utypes = ['Admin', 'Employee']
    for _ in range(n):
        ename = fake.name()
        email = fake.email()
        gender = random.choice(genders)
        contact = fake.phone_number()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=60)
        doj = fake.date_this_decade()
        password = fake.password()
        utype = random.choice(utypes)
        address = fake.address()
        salary = round(random.uniform(30000, 120000), 2)

        try:
            cursor.execute('''INSERT INTO employee (ename, email, gender, contact, dob, doj, pass, utype, address, salary)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                           (ename, email, gender, contact, dob, doj, password, utype, address, salary))
        except sqlite3.Error as e:
            print(f"Error inserting into employee: {e}")
    conn.commit()

# Generate Random Data for Supplier Table
def generate_supplier_data(n=50):
    for _ in range(n):
        name = fake.company()
        contact = fake.phone_number()
        desc = fake.address()

        try:
            cursor.execute('''INSERT INTO supplier (name, contact, desc)
                              VALUES (?, ?, ?)''', (name, contact, desc))
        except sqlite3.Error as e:
            print(f"Error inserting into supplier: {e}")
    conn.commit()

# Generate Random Data for Category Table
def generate_category_data(n=20):
    categories = [fake.word().capitalize() for _ in range(n)]  # Generating unique random category names
    for name in set(categories):  # Ensure no duplicate categories
        try:
            cursor.execute('''INSERT INTO category (name) VALUES (?)''', (name,))
        except sqlite3.Error as e:
            print(f"Error inserting into category: {e}")
    conn.commit()

# Generate Random Data for Product Table
def generate_product_data(n=100):
    cursor.execute("SELECT name FROM category")
    categories = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT name FROM supplier")
    suppliers = [row[0] for row in cursor.fetchall()]

    if not categories or not suppliers:
        print("Please ensure categories and suppliers have been populated first.")
        return

    statuses = ['Active', 'Inactive']
    for _ in range(n):
        category = random.choice(categories)
        supplier = random.choice(suppliers)
        name = fake.word().capitalize() + ' ' + fake.word().capitalize()
        price = round(random.uniform(10, 5000), 2)
        quantity = random.randint(1, 100)
        status = random.choice(statuses)

        try:
            cursor.execute('''INSERT INTO product (category, supplier, name, price, quantity, status)
                              VALUES (?, ?, ?, ?, ?, ?)''',
                           (category, supplier, name, price, quantity, status))
        except sqlite3.Error as e:
            print(f"Error inserting into product: {e}")
    conn.commit()

# Verify Data Insertion
def verify_data():
    tables = ['employee', 'supplier', 'category', 'product']
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"Table {table} has {count} rows.")

# Run the Script
if __name__ == "__main__":
    print("Creating tables...")
    create_tables()

    print("Generating employee data...")
    generate_employee_data(100)

    print("Generating supplier data...")
    generate_supplier_data(50)

    print("Generating category data...")
    generate_category_data(20)

    print("Generating product data...")
    generate_product_data(100)

    print("Verifying data insertion...")
    verify_data()

    print("All data generated successfully!")
    conn.close()
