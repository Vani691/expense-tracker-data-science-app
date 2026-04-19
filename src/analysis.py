import pandas as pd


def category_analysis(df):
    return df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_values(ascending=False)


def monthly_analysis(df):
    monthly = df.groupby("YearMonth")["Amount"].sum()
    return monthly


def income_vs_expense(df):
    summary = df.groupby("Type")["Amount"].sum()
    return summary


def weekday_analysis(df):
    return df.groupby("Weekday")["Amount"].sum()


if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_expenses.csv")

    print("Category Analysis:\n", category_analysis(df))
    print("\nMonthly Analysis:\n", monthly_analysis(df))
    print("\nIncome vs Expense:\n", income_vs_expense(df))
    print("\nWeekday Analysis:\n", weekday_analysis(df))