import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

TOKEN   = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")

headers = {"Authorization": f"Bearer {TOKEN}"}

# ── Helper: fetch all records from a table ─────────────────
def fetch_all_records(table_id):
    records = []
    url = f"https://api.airtable.com/v0/{BASE_ID}/{table_id}"
    params = {}
    while True:
        r = requests.get(url, headers=headers, params=params)
        data = r.json()
        records.extend(data.get('records', []))
        offset = data.get('offset')
        if not offset:
            break
        params['offset'] = offset  # fetch next page
    return [r['fields'] for r in records]

# ── Get table IDs ──────────────────────────────────────────
tables_r = requests.get(f"https://api.airtable.com/v0/meta/bases/{BASE_ID}/tables", headers=headers)
tables   = {t['name']: t['id'] for t in tables_r.json()['tables']}

# ── Fetch live data from Airtable ──────────────────────────
print("Fetching data from Airtable...")
portfolio  = pd.DataFrame(fetch_all_records(tables['Portfolio Companies']))
payments   = pd.DataFrame(fetch_all_records(tables['Monthly Payments']))
covenants  = pd.DataFrame(fetch_all_records(tables['Covenant Checks']))

print(f"Portfolio: {len(portfolio)} loans")
print(f"Payments : {len(payments)} records")
print(f"Covenants: {len(covenants)} records")

# ── ANALYSIS 1: Payment Summary ────────────────────────────
print("\n=== PAYMENT SUMMARY ===")
payment_summary = payments['payment_status'].value_counts()
print(payment_summary)

total_due  = payments['amount_due'].sum()
total_paid = payments['amount_paid'].sum()
collection_rate = (total_paid / total_due) * 100
print(f"\nTotal Due  : ${total_due:,.0f}")
print(f"Total Paid : ${total_paid:,.0f}")
print(f"Collection Rate: {collection_rate:.1f}%")

# ── ANALYSIS 2: Missed Payments — needs immediate action ───
print("\n=== MISSED PAYMENTS (ACTION REQUIRED) ===")
missed = payments[payments['payment_status'] == 'Missed']
print(f"Total missed: {len(missed)}")
print(missed[['borrower_name', 'country', 'due_date', 'amount_due']].to_string(index=False))

# ── ANALYSIS 3: Covenant Breaches ─────────────────────────
print("\n=== COVENANT BREACHES ===")
breaches = covenants[covenants['covenant_status'] == 'Breach']
print(f"Total breaches: {len(breaches)}")
print(breaches[['borrower_name', 'country', 'dscr', 'debt_to_equity']].to_string(index=False))

# ── ANALYSIS 4: Portfolio Health Score ────────────────────
print("\n=== PORTFOLIO HEALTH SCORE ===")
total_loans       = len(portfolio)
breach_count      = len(breaches)
missed_count      = len(missed[missed['due_date'] == missed['due_date'].max()])  # latest month only
compliant_pct     = ((total_loans - breach_count) / total_loans) * 100
on_time_pct       = (payment_summary.get('On Time', 0) / len(payments)) * 100

health_score = (compliant_pct * 0.5) + (on_time_pct * 0.5)

print(f"Loans Compliant     : {compliant_pct:.1f}%")
print(f"Payments On Time    : {on_time_pct:.1f}%")
print(f"Portfolio Health    : {health_score:.1f} / 100")

if health_score >= 80:
    print("Status: HEALTHY ✓")
elif health_score >= 60:
    print("Status: WATCH ⚠")
else:
    print("Status: AT RISK ✗")

# ── Save summary for Claude to use next ───────────────────
summary = {
    "total_loans"       : total_loans,
    "total_aum_usd"     : round(portfolio['loan_amount_usd'].sum(), 2),
    "collection_rate"   : round(collection_rate, 1),
    "on_time_pct"       : round(on_time_pct, 1),
    "missed_payments"   : len(missed),
    "covenant_breaches" : len(breaches),
    "health_score"      : round(health_score, 1),
    "breach_details"    : breaches[['borrower_name', 'country', 'dscr', 'debt_to_equity']].to_dict(orient='records'),
    "missed_details"    : missed[['borrower_name', 'country', 'amount_due']].to_dict(orient='records')
}

import json
with open("portfolio_summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\nSummary saved to portfolio_summary.json")
print("Ready for Claude report generation!")