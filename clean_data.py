import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ── Load raw data ──────────────────────────────────────────
df = pd.read_excel("dfc_portfolio.xlsx", sheet_name="Project Data", header=1)

# ── Apply same filters as before ───────────────────────────
focus_sectors = [
    'Finance and Insurance',
    'Utilities',
    'Health Care and Social Assistance',
    'Agriculture, Forestry, Fishing and Hunting'
]
focus_regions = ['Asia', 'Africa']

portfolio_df = df[
    (df['Project Type'] == 'DI') &
    (df['Region'].isin(focus_regions)) &
    (df['NAICS Sector'].isin(focus_sectors))
].copy()

# ── Keep only useful columns ───────────────────────────────
portfolio_df = portfolio_df[[
    'Project Name',
    'Country',
    'NAICS Sector',
    'Committed',
    'Exposure',
    'Estimated Term (Years)',
    'Fiscal Year'
]].reset_index(drop=True)

# ── Rename columns to fund language ───────────────────────
portfolio_df.rename(columns={
    'Project Name'          : 'borrower_name',
    'Country'               : 'country',
    'NAICS Sector'          : 'sector',
    'Committed'             : 'loan_amount_usd',
    'Exposure'              : 'outstanding_balance',
    'Estimated Term (Years)': 'term_years',
    'Fiscal Year'           : 'fiscal_year'
}, inplace=True)

# ── Filter: only loans above $1M (realistic for our fund) ──
portfolio_df = portfolio_df[portfolio_df['loan_amount_usd'] >= 1_000_000].copy()
portfolio_df = portfolio_df.reset_index(drop=True)

print(f"Clean portfolio: {len(portfolio_df)} loans")
print(portfolio_df.head(10))

# ── Simulate interest rate (real funds assign this) ────────
# Based on sector risk profile
sector_rates = {
    'Finance and Insurance'                        : 0.11,
    'Utilities'                                    : 0.10,
    'Health Care and Social Assistance'            : 0.12,
    'Agriculture, Forestry, Fishing and Hunting'   : 0.13
}
portfolio_df['interest_rate'] = portfolio_df['sector'].map(sector_rates)

# ── Simulate loan start date based on fiscal year ──────────
def fiscal_year_to_date(fy):
    try:
        return datetime(int(fy), 10, 1)  # Oct 1 = US fiscal year start
    except:
        return datetime(2015, 10, 1)

# Fill missing term_years with median value
portfolio_df['term_years'] = portfolio_df['term_years'].fillna(portfolio_df['term_years'].median())
portfolio_df['term_years'] = portfolio_df['term_years'].astype(int)


# Create loan_start_date FIRST from fiscal year
portfolio_df['loan_start_date'] = portfolio_df['fiscal_year'].apply(fiscal_year_to_date)

# Then calculate loan_end_date using it
portfolio_df['loan_end_date'] = portfolio_df.apply(
    lambda r: r['loan_start_date'] + timedelta(days=365 * r['term_years']), axis=1
)


# ── Add loan status ────────────────────────────────────────
portfolio_df['status'] = 'Active'

# ── Save clean portfolio ───────────────────────────────────
portfolio_df.to_csv("portfolio_clean.csv", index=False)
print("\nSaved to portfolio_clean.csv")
print(f"\nFinal shape: {portfolio_df.shape}")
print("\nSample:")
print(portfolio_df[['borrower_name', 'country', 'sector', 'loan_amount_usd', 'interest_rate', 'loan_start_date']].head(10))