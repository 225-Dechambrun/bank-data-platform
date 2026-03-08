import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Bank Data Platform Dashboard", layout="wide")

API_BASE_URL = "http://bank_fastapi:8000"

st.title("Bank Data Platform Dashboard")

st.markdown("Visualization of banking KPIs exposed by FastAPI")

# KPI by type
st.header("Transactions by type")

response_type = requests.get(f"{API_BASE_URL}/kpi/by-type")

if response_type.status_code == 200:

    data_type = response_type.json()
    df_type = pd.DataFrame(data_type)

    st.dataframe(df_type, use_container_width=True)

    st.bar_chart(df_type.set_index("type")["montant_total"])

else:

    st.error("Cannot load /kpi/by-type")

# Daily KPI
st.header("Daily transactions")

response_daily = requests.get(f"{API_BASE_URL}/kpi/daily")

if response_daily.status_code == 200:

    data_daily = response_daily.json()
    df_daily = pd.DataFrame(data_daily)

    st.dataframe(df_daily, use_container_width=True)

    if not df_daily.empty:

        df_daily["date"] = pd.to_datetime(df_daily["date"])
        df_daily = df_daily.sort_values("date")

        st.line_chart(df_daily.set_index("date")["montant_total"])

else:

    st.error("Cannot load /kpi/daily")

# Top customers
st.header("Top customers")

limit = st.slider("Number of customers", 5, 20, 10)

response_customers = requests.get(
    f"{API_BASE_URL}/kpi/top-customers?limit={limit}"
)

if response_customers.status_code == 200:

    data_customers = response_customers.json()
    df_customers = pd.DataFrame(data_customers)

    st.dataframe(df_customers, use_container_width=True)

    if not df_customers.empty:

        st.bar_chart(
            df_customers.set_index("customer_id")["montant_total"]
        )

else:

    st.error("Cannot load /kpi/top-customers")
