import Pyro5.api
from common.data_models import UserTaxData

def main():
    with open("estimator_uri.txt") as f:
        uri = f.read().strip()
    estimator = Pyro5.api.Proxy(uri)

    try:
        method = input("Use TFN to fetch stored data? (Y/N): ").strip().upper()
        if method == 'Y':
            tfn = input("Enter your TFN: ").strip()
            result = estimator.estimate_tax_with_tfn(tfn)
        else:
            person_id = input("Enter your Person ID: ")
            n = int(input("How many income records? (1–26): "))
            income_data = []
            for i in range(n):
                income = float(input(f"Income {i+1}: "))
                withheld = float(input(f"Withheld {i+1}: "))
                income_data.append((income, withheld))
            phic = input("Do you have PHIC? (Y/N): ").strip().lower() == 'y'
            user_data = UserTaxData(person_id, income_data, phic)
            result = estimator.estimate_tax(user_data)

        print("\n--- Tax Return Estimate ---")
        for key, val in result.items():
            print(f"{key}: ${val:.2f}")

    except ValueError as ve:
        print("Error:", ve)
    except Exception as e:
        print("Unexpected error occurred:", e)

if __name__ == "__main__":
    main()
