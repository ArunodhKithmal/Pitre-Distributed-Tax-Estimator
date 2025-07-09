import Pyro5.api
from common.data_models import UserTaxData
from server.estimator_logic import compute_tax_estimate

@Pyro5.api.expose
class Estimator:
    def __init__(self):
        with open("pitd_uri.txt") as f:
            self.pitd_uri = f.read().strip()
        self.pitd_proxy = Pyro5.api.Proxy(self.pitd_uri)

    def estimate_tax(self, user_data):
        if isinstance(user_data, dict):
            user_data = UserTaxData(**user_data)

        print(f"Received data from user {user_data.person_id}")
        for i, (income, withheld) in enumerate(user_data.income_data, 1):
            print(f"Record {i}: Income=${income}, Withheld=${withheld}")
        return compute_tax_estimate(user_data)


    def estimate_tax_with_tfn(self, tfn):
        taxpayer_data = self.pitd_proxy.get_taxpayer_data(tfn)
        if not taxpayer_data:
            raise ValueError("Taxpayer data not found.")
        user_data = UserTaxData(
            person_id=taxpayer_data['person_id'],
            income_data=[(rec[2], rec[3]) for rec in taxpayer_data['payroll_records']],
            has_phic=taxpayer_data['has_phic']
        )
        return self.estimate_tax(user_data)

def main():
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(Estimator)
    print("Estimator Server is ready. URI:", uri)
    with open("estimator_uri.txt", "w") as f:
        f.write(str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    main()
