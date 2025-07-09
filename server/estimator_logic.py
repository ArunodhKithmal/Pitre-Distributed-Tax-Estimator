def compute_tax_estimate(user_data):
    if not user_data.income_data:
        raise ValueError("No income records provided.")

    for i, (income, withheld) in enumerate(user_data.income_data, start=1):
        if income < 0:
            raise ValueError(f"Income in record {i} is negative.")
        if withheld < 0:
            raise ValueError(f"Withheld tax in record {i} is negative.")
        if withheld > income:
            raise ValueError(f"Withheld tax in record {i} exceeds income.")

    income_total = sum(i for i, _ in user_data.income_data)
    withheld_total = sum(w for _, w in user_data.income_data)

    ml = 0.02 * income_total
    mls = 0.0
    if not user_data.has_phic:
        if income_total > 140000:
            mls = 0.015 * income_total
        elif income_total > 105000:
            mls = 0.0125 * income_total
        elif income_total > 90000:
            mls = 0.01 * income_total

    if income_total <= 18200:
        tax = 0
    elif income_total <= 45000:
        tax = 0.19 * (income_total - 18200)
    elif income_total <= 120000:
        tax = 5092 + 0.325 * (income_total - 45000)
    elif income_total <= 180000:
        tax = 29467 + 0.37 * (income_total - 120000)
    else:
        tax = 51667 + 0.45 * (income_total - 180000)

    refund = withheld_total - (tax + ml + mls)
    return {
        "annual_income": income_total,
        "tax_withheld": withheld_total,
        "tax": tax,
        "ml": ml,
        "mls": mls,
        "refund": refund
    }
