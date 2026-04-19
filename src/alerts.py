import pandas as pd


def monthly_expense(df):
    df["Date"] = pd.to_datetime(df["Date"])
    monthly = df[df["Type"] == "Expense"].groupby(df["Date"].dt.to_period("M"))["Amount"].sum()
    return monthly


def check_budget(df, budget=50000):
    monthly = monthly_expense(df)

    alerts = []

    for month, value in monthly.items():
        if value > budget:
            alerts.append(f"⚠️ {month}: Budget exceeded (₹{value})")

    return alerts


def category_budget(df, category_limits):
    df_exp = df[df["Type"] == "Expense"]

    category_spend = df_exp.groupby("Category")["Amount"].sum()

    alerts = []

    for category, limit in category_limits.items():
        if category in category_spend and category_spend[category] > limit:
            alerts.append(
                f"⚠️ {category}: Limit exceeded (₹{category_spend[category]} > ₹{limit})"
            )

    return alerts


def generate_insights(df):
    insights = []

    df_exp = df[df["Type"] == "Expense"]

    # Top category
    top_category = df_exp.groupby("Category")["Amount"].sum().idxmax()
    insights.append(f"💡 Highest spending category: {top_category}")

    # Weekend spending
    weekend = df_exp[df_exp["Is_Weekend"] == True]["Amount"].sum()
    weekday = df_exp[df_exp["Is_Weekend"] == False]["Amount"].sum()

    if weekend > weekday:
        insights.append("💡 You spend more on weekends")

    # Monthly trend
    monthly = monthly_expense(df)
    if monthly.iloc[-1] > monthly.iloc[0]:
        insights.append("💡 Your spending is increasing over time")

    return insights


if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_expenses.csv")

    print("🔔 Budget Alerts:")
    print(check_budget(df, budget=50000))

    print("\n🔔 Category Alerts:")
    limits = {
        "Food": 5000,
        "Shopping": 10000,
        "Travel": 3000
    }
    print(category_budget(df, limits))

    print("\n📊 Insights:")
    print(generate_insights(df))