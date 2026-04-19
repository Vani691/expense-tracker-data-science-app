import pandas as pd


def clean_data(df):
    """
    Cleans raw expense data
    """

    # Remove duplicates
    df = df.drop_duplicates()

    # Handle missing values
    df = df.dropna(subset=["Date", "Amount", "Category", "Type"])

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert Amount
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Drop invalid rows after conversion
    df = df.dropna(subset=["Date", "Amount"])

    # Standardize text columns
    df["Category"] = df["Category"].str.strip().str.title()
    df["Type"] = df["Type"].str.strip().str.title()
    df["Payment_Method"] = df["Payment_Method"].str.strip().str.title()

    return df


def feature_engineering(df):
    """
    Adds new time-based and analytical features
    """

    # Time features
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.month_name()
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.day_name()

    # Weekend flag
    df["Is_Weekend"] = df["Weekday"].isin(["Saturday", "Sunday"])

    # Expense vs Income flag
    df["Is_Expense"] = df["Type"] == "Expense"

    # Monthly aggregation reference
    df["YearMonth"] = df["Date"].dt.to_period("M")

    return df


def save_clean_data(df, path="../data/cleaned_expenses.csv"):
    df.to_csv(path, index=False)
    print("✅ Cleaned data saved!")


if __name__ == "__main__":
    df = pd.read_csv("../data/raw_expenses.csv")

    df = clean_data(df)
    df = feature_engineering(df)

    save_clean_data(df)