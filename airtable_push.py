import requests
import os
from dotenv import load_dotenv

import pandas as pd
import json
import time

# ── Load API keys from .env ────────────────────────────────
load_dotenv()

TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

# ── Test connection ────────────────────────────────────────
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
response = requests.get(url, headers=headers)

print(f"Status code: {response.status_code}")

# ── Load our clean data ────────────────────────────────────
portfolio_df = pd.read_csv("portfolio_clean.csv")
payments_df  = pd.read_csv("payments.csv")
covenants_df = pd.read_csv("covenants.csv")

# ── Helper: create a new table ─────────────────────────────
def create_table(table_name, fields):
    url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
    payload = {"name": table_name, "fields": fields}
    r = requests.post(url, headers=headers, json=payload)
    print(f"Created table '{table_name}': {r.status_code}")
    return r.json().get('id')

# ── Helper: push records in batches of 10 ─────────────────
def push_records(table_id, records):
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_id}"
    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        payload = {"records": [{"fields": r} for r in batch]}

        for attempt in range(3):
            try:
                r = requests.post(url, headers=headers, json=payload)
                if r.status_code != 200:
                    print(f"Error batch {i}: {r.json()}")
                break
            except Exception as e:
                print(f"Retry {attempt+1} for batch {i}...")
                time.sleep(2)

        time.sleep(0.3)

    print(f"Pushed {len(records)} records")

# ── Get or create tables ───────────────────────────────────
tables_url = f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables"
tables_response = requests.get(tables_url, headers=headers)
tables = {t['name']: t['id'] for t in tables_response.json()['tables']}

print("Existing tables:", list(tables.keys()))

# Portfolio Companies — fetch existing
portfolio_table_id = tables['Portfolio Companies']
print(f"Portfolio table ID: {portfolio_table_id}")

# Monthly Payments — recreate since it was deleted
if 'Monthly Payments' in tables:
    payments_table_id = tables['Monthly Payments']
    print("Monthly Payments table found")
else:
    payments_table_id = create_table("Monthly Payments", [
        {"name": "borrower_name",  "type": "singleLineText"},
        {"name": "country",        "type": "singleLineText"},
        {"name": "due_date",       "type": "singleLineText"},
        {"name": "amount_due",     "type": "number", "options": {"precision": 2}},
        {"name": "amount_paid",    "type": "number", "options": {"precision": 2}},
        {"name": "payment_status", "type": "singleLineText"},
    ])
    print("Monthly Payments table created")

# Covenant Checks — fetch existing
covenants_table_id = tables['Covenant Checks']
print(f"Covenant table ID: {covenants_table_id}")

# ── Push payments only ─────────────────────────────────────
print("\nPushing Monthly Payments...")
push_records(payments_table_id, payments_df.to_dict(orient='records'))

print("\nAll data pushed to Airtable!")