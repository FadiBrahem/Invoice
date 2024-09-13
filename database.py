import sqlite3

class Database:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                amount REAL NOT NULL
            )
        ''')
        self.conn.commit()
    
    def insert_invoice(self, customer, amount):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO invoices (customer, amount) VALUES (?, ?)
        ''', (customer, amount))
        self.conn.commit()
        return cursor.lastrowid
    
    def fetch_invoices(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM invoices')
        return cursor.fetchall()
