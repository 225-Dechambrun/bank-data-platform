# -*- coding: utf-8 -*-
import os
import pandas as pd
import requests

os.makedirs("dashboard/data", exist_ok=True)

pd.DataFrame(requests.get("http://localhost:8000/kpi/by-type").json()).to_csv("dashboard/data/kpi_by_type.csv", index=False)
pd.DataFrame(requests.get("http://localhost:8000/kpi/daily").json()).to_csv("dashboard/data/kpi_daily.csv", index=False)
pd.DataFrame(requests.get("http://localhost:8000/kpi/top-customers?limit=20").json()).to_csv("dashboard/data/kpi_top_customers.csv", index=False)

print("CSV files created successfully.")
