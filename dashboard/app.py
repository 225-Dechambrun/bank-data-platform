from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Bank Data Platform Dashboard", layout="wide")

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

st.title("Bank Data Platform Dashboard")
st.markdown("Visualization of banking KPIs from local CSV files")

def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        st.error(f"File not found: {path}")
        st.stop()

    df = pd.read_csv(path)

    # Nettoyage des noms de colonnes
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )

    return df

# KPI by type
st.header("Transactions by type")
df_type = load_csv("kpi_by_type.csv")

st.write("Columns in kpi_by_type.csv :", list(df_type.columns))
st.dataframe(df_type, width="stretch")

if not df_type.empty and "type" in df_type.columns and "montant_total" in df_type.columns:
    st.bar_chart(df_type.set_index("type")["montant_total"])
else:
    st.error(f"Expected columns: type, montant_total | Found: {list(df_type.columns)}")

# Daily KPI
st.header("Daily transactions")
df_daily = load_csv("kpi_daily.csv")

st.write("Columns in kpi_daily.csv :", list(df_daily.columns))
st.dataframe(df_daily, width="stretch")

if not df_daily.empty and "date" in df_daily.columns and "montant_total" in df_daily.columns:
    df_daily["date"] = pd.to_datetime(df_daily["date"])
    df_daily = df_daily.sort_values("date")
    st.line_chart(df_daily.set_index("date")["montant_total"])
else:
    st.error(f"Expected columns: date, montant_total | Found: {list(df_daily.columns)}")

# Top customers
st.header("Top customers")
df_customers = load_csv("kpi_top_customers.csv")

st.write("Columns in kpi_top_customers.csv :", list(df_customers.columns))

limit = st.slider("Number of customers", 5, 20, 10)
df_customers_display = df_customers.head(limit)

st.dataframe(df_customers_display, width="stretch")

if not df_customers_display.empty and "customer_id" in df_customers_display.columns and "montant_total" in df_customers_display.columns:
    st.bar_chart(df_customers_display.set_index("customer_id")["montant_total"])
else:
    st.error(f"Expected columns: customer_id, montant_total | Found: {list(df_customers_display.columns)}")
