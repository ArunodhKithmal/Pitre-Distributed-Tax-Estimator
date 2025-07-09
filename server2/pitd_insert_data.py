import sqlite3

def insert_sample_data():
    conn = sqlite3.connect('pitd_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO taxpayers (tfn, person_id, has_phic)
        VALUES ('123456789', '123456', 1)
    ''')
    payroll_data = [
        ('123456789', '2024-Q1', '2024-03-31', 2000.00, 300.00),
        ('123456789', '2024-Q2', '2024-06-30', 2100.00, 350.00),
    ]
    cursor.executemany('''
        INSERT INTO payroll_records (tfn, pay_period, payday, gross_income, tax_withheld)
        VALUES (?, ?, ?, ?, ?)
    ''', payroll_data)
    conn.commit()
    conn.close()

insert_sample_data()
