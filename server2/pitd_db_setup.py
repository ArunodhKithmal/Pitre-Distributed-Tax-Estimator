import sqlite3

def initialize_database():
    conn = sqlite3.connect('pitd_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS taxpayers (
            tfn TEXT PRIMARY KEY,
            person_id TEXT UNIQUE,
            has_phic BOOLEAN
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payroll_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tfn TEXT,
            pay_period TEXT,
            payday DATE,
            gross_income REAL,
            tax_withheld REAL,
            FOREIGN KEY (tfn) REFERENCES taxpayers (tfn)
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()
