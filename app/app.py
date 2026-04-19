import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd

from src.analysis import category_analysis
from src.alerts import generate_insights, check_budget
from src.ml_model import prepare_data, train_model, make_future

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Expense Tracker", layout="wide")

# ------------------ LOAD DATA ------------------
df = pd.read_csv("data/cleaned_expenses.csv")
df["Date"] = pd.to_datetime(df["Date"])

# ------------------ SIDEBAR ------------------
st.sidebar.title("🔍 Filters")

# -------- FILTER SECTION --------
with st.sidebar.expander("📂 Filter Data", expanded=True):
    category = st.multiselect(
        "Category",
        options=sorted(df["Category"].unique()),
        default=sorted(df["Category"].unique())
    )

    date_range = st.date_input(
        "Date Range",
        [df["Date"].min(), df["Date"].max()]
    )

# -------- ADD EXPENSE --------
with st.sidebar.expander("➕ Add Expense"):
    with st.form("add_expense_form"):
        date = st.date_input("Date")

        category_input = st.selectbox(
            "Category",
            sorted(df["Category"].unique())
        )

        # 🔥 Slider + manual input combo
        amount_slider = st.slider("Amount (Quick Select)", 0, 20000, 500)
        amount_manual = st.number_input("Or enter exact amount", min_value=0, value=amount_slider)

        payment = st.selectbox("Payment Method", ["UPI", "Card", "Cash"])

        submit = st.form_submit_button("Add Expense")

        if submit:
            new_row = pd.DataFrame([{
                "Date": date,
                "Category": category_input,
                "Amount": amount_manual,
                "Type": "Expense",
                "Payment_Method": payment
            }])

            df = pd.concat([df, new_row], ignore_index=True)
            st.success("Expense added successfully!")

# -------- FILE UPLOAD --------
with st.sidebar.expander("📤 Upload Data"):
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        new_data = pd.read_csv(uploaded_file)
        new_data["Date"] = pd.to_datetime(new_data["Date"])

        df = pd.concat([df, new_data], ignore_index=True)
        st.success("Data uploaded successfully!")

# ------------------ FILTER DATA ------------------
filtered_df = df[
    (df["Category"].isin(category)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

# ------------------ HEADER ------------------
st.title("💰 Expense Tracker Dashboard")
st.markdown("---")

# ------------------ KPIs ------------------
total_expense = filtered_df[filtered_df["Type"] == "Expense"]["Amount"].sum()
total_income = filtered_df[filtered_df["Type"] == "Income"]["Amount"].sum()
net_balance = total_income - total_expense

col1, col2, col3 = st.columns(3)

col1.metric("💸 Total Expense", f"₹{total_expense:,.0f}")
col2.metric("💰 Total Income", f"₹{total_income:,.0f}")
col3.metric("📊 Net Balance", f"₹{net_balance:,.0f}")

st.markdown("---")

# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Category Spending")
    cat_data = category_analysis(filtered_df)
    st.bar_chart(cat_data)

with col2:
    st.subheader("📈 Monthly Trend")
    monthly = filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Amount"].sum()
    st.line_chart(monthly)

st.markdown("---")

# ------------------ FORECAST ------------------
st.subheader("🔮 Expense Forecast")

data = prepare_data(filtered_df)
model = train_model(data)
forecast = make_future(model)

st.line_chart(forecast.set_index("ds")["yhat"])

st.markdown("---")

# ------------------ ALERTS ------------------
st.subheader("🚨 Alerts")

# Global alerts (full dataset)
global_alerts = check_budget(df, budget=50000)

# Filtered alerts
filtered_alerts = check_budget(filtered_df, budget=50000)

if global_alerts:
    st.markdown("### 🌍 Overall Alerts")
    for alert in global_alerts:
        st.warning(alert)

if filtered_alerts:
    st.markdown("### 🎯 Filtered Alerts")
    for alert in filtered_alerts:
        st.warning(alert)

if not global_alerts and not filtered_alerts:
    st.success("No budget issues detected ✅")

# ------------------ INSIGHTS ------------------
st.subheader("💡 Insights")

insights = generate_insights(filtered_df)
for insight in insights:
    st.info(insight)