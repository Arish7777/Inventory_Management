import sqlite3
def create_connection():
        conn = sqlite3.connect(database=r'DB PROJECT.db')
        cur = conn.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS employee (eid INTEGER PRIMARY KEY AUTOINCREMENT, ename TEXT, email TEXT, gender TEXT, contact TEXT, dob TEXT, doj TEXT,pass TEXT,utype TEXT, address TEXT, salary INTEGER)')
        conn.commit()

        cur.execute('CREATE TABLE IF NOT EXISTS supplier (invoice INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, contact TEXT, desc TEXT)')
        conn.commit()

        cur.execute('CREATE TABLE IF NOT EXISTS category (cid INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)')
        conn.commit()

        cur.execute('CREATE TABLE IF NOT EXISTS product (pid INTEGER PRIMARY KEY AUTOINCREMENT, Category TEXT, Supplier TEXT, name TEXT, price TEXT, quantity TEXT, status TEXT)')
        conn.commit()

        

create_connection()

