import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set(style="whitegrid")


def save_plot(fig, filename):
    os.makedirs("../outputs/charts", exist_ok=True)
    fig.savefig(f"../outputs/charts/{filename}", bbox_inches="tight")
    print(f"✅ Saved: {filename}")


def plot_category_spending(df):
    data = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum().sort_values()

    fig = plt.figure(figsize=(10, 5))
    data.plot(kind="barh")
    plt.title("Category-wise Spending")
    plt.xlabel("Amount")
    plt.ylabel("Category")

    save_plot(fig, "category_spending.png")
    plt.close()


def plot_expense_distribution(df):
    data = df[df["Type"] == "Expense"].groupby("Category")["Amount"].sum()

    fig = plt.figure(figsize=(7, 7))
    plt.pie(data, labels=data.index, autopct="%1.1f%%")
    plt.title("Expense Distribution")

    save_plot(fig, "expense_distribution.png")
    plt.close()


def plot_monthly_trend(df):
    df["YearMonth"] = df["Date"].astype(str).str[:7]
    data = df.groupby("YearMonth")["Amount"].sum()

    fig = plt.figure(figsize=(10, 5))
    data.plot(marker="o")
    plt.title("Monthly Trend")
    plt.xlabel("Month")
    plt.ylabel("Amount")

    save_plot(fig, "monthly_trend.png")
    plt.xticks(rotation=45)
    plt.close()


def plot_weekday_spending(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    data = df.groupby("Weekday")["Amount"].sum().reindex(order)

    fig = plt.figure(figsize=(10, 5))
    sns.barplot(x=data.index, y=data.values)
    plt.title("Spending by Weekday")
    plt.xticks(rotation=45)

    save_plot(fig, "weekday_spending.png")
    plt.close()


if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_expenses.csv")

    plot_category_spending(df)
    plot_expense_distribution(df)
    plot_monthly_trend(df)
    plot_weekday_spending(df)