import requests
import pandas as pd

print("Downloading DFC portfolio data...")

url = "https://www.dfc.gov/sites/default/files/media/documents/FY24%20DFC%20Annual%20Project%20Data_508.xlsx"

response = requests.get(url)

with open("dfc_portfolio.xlsx", "wb") as f:
    f.write(response.content)

print("Download complete!")

xl = pd.ExcelFile("dfc_portfolio.xlsx")
print("Sheets available:")
print(xl.sheet_names)

# Read with correct header row
df = pd.read_excel("dfc_portfolio.xlsx", sheet_name="Project Data", header=1)

print("\n--- Shape (rows, columns) ---")
print(df.shape)

print("\n--- Column Names ---")
for col in df.columns.tolist():
    print(col)

print("\n--- First 3 rows ---")
pd.set_option('display.max_columns', None)
print(df.head(3))

# --- Basic exploration ---
print("=== SECTORS ===")
print(df['NAICS Sector'].value_counts().head(10))

print("\n=== REGIONS ===")
print(df['Region'].value_counts())

print("\n=== PROJECT TYPES ===")
print(df['Project Type'].value_counts())

print("\n=== COMMITTED AMOUNT (USD) ===")
print(df['Committed'].describe())

# --- Filter to only Debt loans (most relevant for our fund) ---
debt_df = df[df['Project Type'] == 'DL']  # DL = Direct Lending
print(f"\n=== DEBT LOANS ONLY: {len(debt_df)} records ===")
print(debt_df[['Project Name', 'Country', 'NAICS Sector', 'Committed', 'Estimated Term (Years)']].head(10))

# --- Fix: correct project type codes ---
print("\n=== DIRECT INVESTMENT LOANS (DI) ===")
di_df = df[df['Project Type'] == 'DI']
print(f"Total DI loans: {len(di_df)}")
print(di_df[['Project Name', 'Country', 'NAICS Sector', 'Committed', 'Estimated Term (Years)']].head(10))

# --- Our fund focus: Asia + Africa, sectors we care about ---
print("\n=== FILTERED: Asia/Africa, Finance+Utilities+Health+Agriculture ===")
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
]

print(f"Portfolio size: {len(portfolio_df)} loans")
print(portfolio_df[['Project Name', 'Country', 'NAICS Sector', 'Committed', 'Estimated Term (Years)']].head(15))