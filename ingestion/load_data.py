import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://data:data@127.0.0.1:5432/bank")

customers = pd.read_csv("data/customers.csv")
accounts = pd.read_csv("data/accounts.csv")
transactions = pd.read_csv("data/transactions.csv")

customers.to_sql("customers_raw", engine, if_exists="replace", index=False)
accounts.to_sql("accounts_raw", engine, if_exists="replace", index=False)
transactions.to_sql("transactions_raw", engine, if_exists="replace", index=False)

print("Data loaded successfully into PostgreSQL")
