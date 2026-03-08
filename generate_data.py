# -*- coding: utf-8 -*-
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

first_names = [
    "Stephane", "Marie", "Paul", "Sara", "Jean", "Amina", "Lucas", "Fatou",
    "Eric", "Nina", "Kevin", "Sophie", "Yao", "Emma", "Moussa", "Ines"
]

last_names = [
    "Dupont", "Martin", "Bernard", "Diallo", "Kone", "Traore", "Moreau",
    "Garcia", "Petit", "Leroy", "Kouassi", "Ba", "Durand", "Lopez", "Ndiaye"
]

countries = [
    "France", "Germany", "Spain", "Italy", "Belgium",
    "Portugal", "Netherlands", "Luxembourg"
]

account_types = ["current", "savings"]
transaction_types = ["payment", "transfer", "withdrawal", "deposit"]

customers = []
num_customers = 200

for customer_id in range(1, num_customers + 1):
    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    age = random.randint(18, 70)
    country = random.choice(countries)
    customers.append([customer_id, name, age, country])

with open(data_dir / "customers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["customer_id", "name", "age", "country"])
    writer.writerows(customers)

accounts = []
num_accounts = 300

for account_id in range(1, num_accounts + 1):
    customer_id = random.randint(1, num_customers)
    acc_type = random.choice(account_types)
    balance = random.randint(500, 50000)
    accounts.append([account_id, customer_id, acc_type, balance])

with open(data_dir / "accounts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["account_id", "customer_id", "type", "balance"])
    writer.writerows(accounts)

transactions = []
num_transactions = 10000
start_date = datetime(2025, 1, 1)

for transaction_id in range(1, num_transactions + 1):
    account_id = random.randint(1, num_accounts)
    tx_type = random.choice(transaction_types)

    if tx_type == "withdrawal":
        amount = round(random.uniform(20, 1000), 2)
    elif tx_type == "payment":
        amount = round(random.uniform(5, 3000), 2)
    elif tx_type == "transfer":
        amount = round(random.uniform(50, 10000), 2)
    else:
        amount = round(random.uniform(50, 15000), 2)

    tx_date = start_date + timedelta(days=random.randint(0, 364))
    transactions.append([
        transaction_id,
        account_id,
        amount,
        tx_type,
        tx_date.strftime("%Y-%m-%d")
    ])

with open(data_dir / "transactions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["transaction_id", "account_id", "amount", "type", "date"])
    writer.writerows(transactions)

print("Files generated successfully:")
print("customers.csv :", num_customers, "rows")
print("accounts.csv :", num_accounts, "rows")
print("transactions.csv :", num_transactions, "rows")
