import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os


def prepare_data(df):
    """
    Convert ONLY expense data to Prophet format
    """

    df["Date"] = pd.to_datetime(df["Date"])

    # ✅ Filter ONLY expenses
    df = df[df["Type"] == "Expense"]

    # Monthly aggregation
    monthly = df.groupby(df["Date"].dt.to_period("M"))["Amount"].sum().reset_index()

    monthly["Date"] = monthly["Date"].astype(str)

    # Prophet format
    monthly.rename(columns={"Date": "ds", "Amount": "y"}, inplace=True)

    monthly["ds"] = pd.to_datetime(monthly["ds"])

    return monthly


def train_model(data):
    model = Prophet()
    model.fit(data)
    return model


def make_future(model, periods=3):
    future = model.make_future_dataframe(periods=periods, freq="ME")
    forecast = model.predict(future)
    return forecast


def plot_forecast(model, forecast):
    fig = model.plot(forecast)

    os.makedirs("../outputs/charts", exist_ok=True)
    fig.savefig("../outputs/charts/forecast.png")

    print("✅ Forecast saved!")


if __name__ == "__main__":
    df = pd.read_csv("../data/cleaned_expenses.csv")

    data = prepare_data(df)
    model = train_model(data)
    forecast = make_future(model)

    plot_forecast(model, forecast)