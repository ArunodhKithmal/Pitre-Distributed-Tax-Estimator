import Pyro5.api
import sqlite3

@Pyro5.api.expose
class PITDDatabase:
    def get_taxpayer_data(self, tfn):
        conn = sqlite3.connect('pitd_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT person_id, has_phic FROM taxpayers WHERE tfn = ?', (tfn,))
        taxpayer = cursor.fetchone()
        if not taxpayer:
            return None
        person_id, has_phic = taxpayer
        cursor.execute('SELECT pay_period, payday, gross_income, tax_withheld FROM payroll_records WHERE tfn = ?', (tfn,))
        payroll_records = cursor.fetchall()
        conn.close()
        return {
            'person_id': person_id,
            'has_phic': bool(has_phic),
            'payroll_records': payroll_records
        }

def main():
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(PITDDatabase)
    print("PITD Server is ready. URI:", uri)
    with open("pitd_uri.txt", "w") as f:
        f.write(str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    main()
