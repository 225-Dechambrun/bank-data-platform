import psycopg2

conn = psycopg2.connect(
    host="postgres",
    dbname="bank",
    user="data",
    password="data"
)

cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS customers_raw;
CREATE TABLE customers_raw (
    customer_id INT,
    name TEXT,
    age INT,
    country TEXT
);

DROP TABLE IF EXISTS accounts_raw;
CREATE TABLE accounts_raw (
    account_id INT,
    customer_id INT,
    type TEXT,
    balance INT
);

DROP TABLE IF EXISTS transactions_raw;
CREATE TABLE transactions_raw (
    transaction_id INT,
    account_id INT,
    amount NUMERIC,
    type TEXT,
    date DATE
);
""")

with open("/opt/airflow/data/customers.csv", "r", encoding="utf-8") as f:
    cur.copy_expert(
        "COPY customers_raw FROM STDIN WITH CSV HEADER",
        f
    )

with open("/opt/airflow/data/accounts.csv", "r", encoding="utf-8") as f:
    cur.copy_expert(
        "COPY accounts_raw FROM STDIN WITH CSV HEADER",
        f
    )

with open("/opt/airflow/data/transactions.csv", "r", encoding="utf-8") as f:
    cur.copy_expert(
        "COPY transactions_raw FROM STDIN WITH CSV HEADER",
        f
    )

conn.commit()
cur.close()
conn.close()

print("Raw data loaded successfully")
