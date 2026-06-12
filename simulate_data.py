import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ── Load clean portfolio ───────────────────────────────────
df = pd.read_csv("portfolio_clean.csv")

print(f"Loaded {len(df)} loans")

random.seed(42)  # Makes results reproducible

# ── TABLE 1: Monthly Payments ──────────────────────────────
# For each loan, simulate last 3 months of payments
payment_records = []

for _, row in df.iterrows():
    monthly_payment = round((row['loan_amount_usd'] * row['interest_rate']) / 12, 2)

    for month_offset in [3, 2, 1]:  # 3 months ago, 2 months ago, last month
        due_date = datetime(2026, 6, 1) - timedelta(days=30 * month_offset)

        # Simulate payment behavior — 80% on time, 10% late, 10% missed
        outcome = random.choices(
            ['On Time', 'Late', 'Missed'],
            weights=[80, 10, 10]
        )[0]

        if outcome == 'On Time':
            amount_paid = monthly_payment
        elif outcome == 'Late':
            amount_paid = monthly_payment  # paid but late
        else:
            amount_paid = 0  # missed

        payment_records.append({
            'borrower_name'  : row['borrower_name'],
            'country'        : row['country'],
            'due_date'       : due_date.strftime('%Y-%m-%d'),
            'amount_due'     : monthly_payment,
            'amount_paid'    : amount_paid,
            'payment_status' : outcome
        })

payments_df = pd.DataFrame(payment_records)
payments_df.to_csv("payments.csv", index=False)
print(f"\nPayments table: {len(payments_df)} records")
print(payments_df['payment_status'].value_counts())
print(payments_df.head(6))

# ── TABLE 2: Covenant Checks ───────────────────────────────
# For each loan, simulate latest covenant check
covenant_records = []

for _, row in df.iterrows():
    # Simulate DSCR — most healthy, some borderline, few breach
    dscr = round(random.choices(
        [random.uniform(1.25, 2.5),   # healthy
         random.uniform(1.0, 1.25),   # borderline
         random.uniform(0.7, 1.0)],   # breach
        weights=[75, 15, 10]
    )[0], 2)

    # Simulate Debt-to-Equity
    dte = round(random.choices(
        [random.uniform(1.0, 2.8),   # healthy
         random.uniform(2.8, 3.0),   # borderline
         random.uniform(3.0, 4.5)],  # breach
        weights=[75, 15, 10]
    )[0], 2)

    # Covenant status — breach if either metric fails
    if dscr < 1.25 or dte > 3.0:
        covenant_status = 'Breach'
    else:
        covenant_status = 'Compliant'

    covenant_records.append({
        'borrower_name'   : row['borrower_name'],
        'country'         : row['country'],
        'check_date'      : '2026-05-01',
        'dscr'            : dscr,
        'debt_to_equity'  : dte,
        'covenant_status' : covenant_status
    })

covenants_df = pd.DataFrame(covenant_records)
covenants_df.to_csv("covenants.csv", index=False)
print(f"\nCovenants table: {len(covenants_df)} records")
print(covenants_df['covenant_status'].value_counts())
print(covenants_df.head(6))

print("\nAll simulation files saved!")