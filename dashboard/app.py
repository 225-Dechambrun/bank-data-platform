from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Bank Data Platform Dashboard",
    page_icon="🏦",
    layout="wide"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

def load_csv(filename):
    path = DATA_DIR / filename
    if not path.exists():
        st.error(f"File not found: {path}")
        st.stop()

    df = pd.read_csv(path)
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
    )
    return df

def format_amount(x):
    try:
        return f"{float(x):,.2f}".replace(",", " ")
    except Exception:
        return x

def card(title, value):
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0f172a, #1e3a8a);
            padding: 18px;
            border-radius: 18px;
            color: white;
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
            margin-bottom: 10px;
        ">
            <div style="font-size: 14px; opacity: 0.85;">{title}</div>
            <div style="font-size: 28px; font-weight: 700; margin-top: 8px;">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# CSS
st.markdown("""
<style>
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}
h1, h2, h3 {
    letter-spacing: 0.2px;
}
[data-testid="stSidebar"] {
    background: #f8fafc;
}
div[data-testid="stMetric"] {
    background-color: #ffffff;
    border: 1px solid #e5e7eb;
    padding: 12px;
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

# Load data
df_type = load_csv("kpi_by_type.csv")
df_daily = load_csv("kpi_daily.csv")
df_customers = load_csv("kpi_top_customers.csv")

if "date" in df_daily.columns:
    df_daily["date"] = pd.to_datetime(df_daily["date"], errors="coerce")
    df_daily = df_daily.sort_values("date")

# Sidebar
st.sidebar.title("⚙️ Dashboard Filters")

available_types = df_type["type"].dropna().unique().tolist() if "type" in df_type.columns else []
selected_types = st.sidebar.multiselect(
    "Transaction types",
    options=available_types,
    default=available_types
)

top_n = st.sidebar.slider("Top customers", 5, 20, 10)

show_tables = st.sidebar.toggle("Show detailed tables", value=True)

# Filters
df_type_filtered = df_type[df_type["type"].isin(selected_types)] if selected_types else df_type.iloc[0:0]
df_customers_display = df_customers.head(top_n).copy()

# KPIs
total_transactions = int(df_type_filtered["nb_transactions"].sum()) if not df_type_filtered.empty else 0
total_amount = float(df_type_filtered["montant_total"].sum()) if not df_type_filtered.empty else 0.0
avg_amount = total_amount / total_transactions if total_transactions > 0 else 0.0
active_days = int(df_daily["date"].nunique()) if "date" in df_daily.columns else 0

# Header
st.markdown("""
<div style="padding: 8px 0 18px 0;">
    <h1 style="margin-bottom: 0;">🏦 Bank Data Platform Dashboard</h1>
    <p style="color: #475569; margin-top: 6px;">
        Premium view of banking KPIs generated from local CSV files
    </p>
</div>
""", unsafe_allow_html=True)

# KPI cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    card("Total transactions", f"{total_transactions:,}".replace(",", " "))
with c2:
    card("Total amount", format_amount(total_amount))
with c3:
    card("Average amount", format_amount(avg_amount))
with c4:
    card("Active days", f"{active_days}")

st.markdown("")

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📋 Detailed Data", "💡 Insights"])

with tab1:
    left, right = st.columns(2)

    with left:
        st.subheader("Transactions by type")
        if not df_type_filtered.empty and "type" in df_type_filtered.columns and "montant_total" in df_type_filtered.columns:
            st.bar_chart(df_type_filtered.set_index("type")["montant_total"])
        else:
            st.warning("No data available for selected transaction types.")

    with right:
        st.subheader("Daily transaction amount")
        if not df_daily.empty and "date" in df_daily.columns and "montant_total" in df_daily.columns:
            st.line_chart(df_daily.set_index("date")["montant_total"])
        else:
            st.warning("Daily KPI data is unavailable.")

    st.markdown("### 👑 Top customers")
    if not df_customers_display.empty and "customer_id" in df_customers_display.columns and "montant_total" in df_customers_display.columns:
        st.bar_chart(df_customers_display.set_index("customer_id")["montant_total"])
    else:
        st.warning("Top customer data is unavailable.")

with tab2:
    if show_tables:
        with st.expander("Transactions by type", expanded=True):
            df_type_table = df_type_filtered.copy()
            if "montant_total" in df_type_table.columns:
                df_type_table["montant_total"] = df_type_table["montant_total"].map(format_amount)
            if "montant_moyen" in df_type_table.columns:
                df_type_table["montant_moyen"] = df_type_table["montant_moyen"].map(format_amount)
            st.dataframe(df_type_table, width="stretch", hide_index=True)

        with st.expander("Daily transactions", expanded=False):
            df_daily_table = df_daily.copy()
            if "date" in df_daily_table.columns:
                df_daily_table["date"] = df_daily_table["date"].dt.strftime("%Y-%m-%d")
            if "montant_total" in df_daily_table.columns:
                df_daily_table["montant_total"] = df_daily_table["montant_total"].map(format_amount)
            if "montant_moyen" in df_daily_table.columns:
                df_daily_table["montant_moyen"] = df_daily_table["montant_moyen"].map(format_amount)
            st.dataframe(df_daily_table, width="stretch", hide_index=True)

        with st.expander("Top customers", expanded=False):
            df_customers_table = df_customers_display.copy()
            if "montant_total" in df_customers_table.columns:
                df_customers_table["montant_total"] = df_customers_table["montant_total"].map(format_amount)
            if "montant_moyen" in df_customers_table.columns:
                df_customers_table["montant_moyen"] = df_customers_table["montant_moyen"].map(format_amount)
            st.dataframe(df_customers_table, width="stretch", hide_index=True)
    else:
        st.info("Enable 'Show detailed tables' in the sidebar to display the tables.")

with tab3:
    st.subheader("Quick insights")

    if not df_type_filtered.empty and "montant_total" in df_type_filtered.columns and "type" in df_type_filtered.columns:
        top_type_row = df_type_filtered.sort_values("montant_total", ascending=False).iloc[0]
        st.success(f"Top transaction type: {top_type_row['type']} with {format_amount(top_type_row['montant_total'])}")

    if not df_customers_display.empty and "montant_total" in df_customers_display.columns and "customer_id" in df_customers_display.columns:
        top_customer_row = df_customers_display.sort_values("montant_total", ascending=False).iloc[0]
        st.info(f"Top customer: #{top_customer_row['customer_id']} with {format_amount(top_customer_row['montant_total'])}")

    if not df_daily.empty and "montant_total" in df_daily.columns and "date" in df_daily.columns:
        best_day_row = df_daily.sort_values("montant_total", ascending=False).iloc[0]
        st.warning(f"Best day: {best_day_row['date'].strftime('%Y-%m-%d')} with {format_amount(best_day_row['montant_total'])}")

st.markdown("---")
st.caption("Data source: local CSV files generated from the banking pipeline")
