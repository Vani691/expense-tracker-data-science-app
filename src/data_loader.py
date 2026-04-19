import pandas as pd
import numpy as np

def generate_synthetic_data(num_days=180):
    np.random.seed(42)

    dates = pd.date_range(end=pd.Timestamp.today(), periods=num_days)

    categories = ["Food", "Rent", "Travel", "Shopping", "Bills", "Entertainment"]
    payment_methods = ["UPI", "Card", "Cash"]

    data = []

    for date in dates:
        # Income (salary once per month)
        if date.day == 1:
            data.append([
                date,
                "Salary",
                np.random.randint(30000, 60000),
                "Income",
                "Bank Transfer"
            ])

        # Daily expenses (1–3 transactions per day)
        for _ in range(np.random.randint(1, 4)):
            category = np.random.choice(categories)

            # Base amount
            if category == "Food":
                amount = np.random.randint(100, 500)
            elif category == "Rent":
                amount = 0
                if date.day == 5:
                    amount = np.random.randint(8000, 15000)
            elif category == "Travel":
                amount = np.random.randint(50, 300)
            elif category == "Shopping":
                amount = np.random.randint(500, 3000)
            elif category == "Bills":
                amount = np.random.randint(500, 2000)
            else:
                amount = np.random.randint(200, 1500)

            # Weekend boost
            if date.weekday() >= 5:
                amount *= 1.2

            # Skip zero rent days
            if amount == 0:
                continue

            data.append([
                date,
                category,
                round(amount, 2),
                "Expense",
                np.random.choice(payment_methods)
            ])

    df = pd.DataFrame(data, columns=[
        "Date", "Category", "Amount", "Type", "Payment_Method"
    ])

    return df


def load_data(file_path=None):
    if file_path:
        df = pd.read_csv(file_path)
    else:
        df = generate_synthetic_data()

    return df


if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv("data/raw_expenses.csv", index=False)
    print("✅ Synthetic dataset generated and saved!")