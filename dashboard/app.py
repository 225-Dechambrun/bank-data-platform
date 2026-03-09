import os
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Bank Data Platform Dashboard", layout="wide")

API_BASE_URL = os.getenv("API_BASE_URL")

if not API_BASE_URL:
    try:
        API_BASE_URL = st.secrets["API_BASE_URL"]
    except Exception:
        API_BASE_URL = "http://localhost:8000"

st.title("Bank Data Platform Dashboard")
st.markdown("Visualization of banking KPIs exposed by FastAPI")


def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot load {endpoint} : {e}")
        return None


st.header("Transactions by type")
data_type = fetch_data("/kpi/by-type")

if data_type is not None:
    df_type = pd.DataFrame(data_type)
    st.dataframe(df_type, width="stretch")

    if not df_type.empty:
        st.bar_chart(df_type.set_index("type")["montant_total"])


st.header("Daily transactions")
data_daily = fetch_data("/kpi/daily")

if data_daily is not None:
    df_daily = pd.DataFrame(data_daily)
    st.dataframe(df_daily, width="stretch")

    if not df_daily.empty:
        df_daily["date"] = pd.to_datetime(df_daily["date"])
        df_daily = df_daily.sort_values("date")
        st.line_chart(df_daily.set_index("date")["montant_total"])


st.header("Top customers")
limit = st.slider("Number of customers", 5, 20, 10)

data_customers = fetch_data(f"/kpi/top-customers?limit={limit}")

if data_customers is not None:
    df_customers = pd.DataFrame(data_customers)
    st.dataframe(df_customers, width="stretch")

    if not df_customers.empty:
        st.bar_chart(df_customers.set_index("customer_id")["montant_total"])
