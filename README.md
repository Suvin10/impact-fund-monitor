# Impact Fund Portfolio Monitor

An end-to-end portfolio monitoring system for an impact debt fund, built with Python, Airtable, and AI.

## What It Does
- Downloads real U.S. DFC impact loan portfolio data (1,300+ loans)
- Cleans and filters to 243 relevant Asia/Africa loans
- Simulates monthly payment tracking and covenant compliance checks
- Pushes all data to Airtable for live monitoring
- Runs automated portfolio health analysis
- Generates charts and visualizations
- Uses AI (Groq/LLaMA) to auto-generate monthly investor reports
- Produces a client-ready Word document with full analysis

## Portfolio Health Output
- Collection Rate: 92.6%
- On-Time Payment Rate: 80.0%
- Covenant Breaches: 63 loans flagged
- Portfolio Health Score: 77/100 (WATCH status)

## Tech Stack
- Python (pandas, requests, matplotlib, python-docx)
- Airtable API
- Groq API (LLaMA 3.3)
- Real data: U.S. International Development Finance Corporation (DFC)

## File Structure
| File | Purpose |
|------|---------|
| download_data.py | Downloads and explores raw DFC data |
| clean_data.py | Cleans and shapes portfolio data |
| simulate_data.py | Simulates payment and covenant data |
| airtable_push.py | Pushes all data to Airtable via API |
| covenant_check.py | Live analysis — flags breaches and missed payments |
| report_generator.py | AI generates monthly investor report and action plan |
| visualize.py | Generates portfolio charts and graphs |
| generate_docx.py | Creates client-ready Word document with charts and analysis |

## Output Files
| File | Description |
|------|-------------|
| investor_report_may2026.txt | AI-generated monthly investor report |
| action_plan_may2026.txt | Fund manager action plan with specific borrower actions |
| Impact_Fund_Portfolio_Report_May2026.docx | Full client-ready Word document with charts and analysis |

## Charts Generated
- Portfolio Health Metrics
- Payment Status Distribution
- Covenant Compliance Status
- Loans by Sector
- Top 10 Countries by Loan Count

## How to Run
```bash
# Step 1: Download and explore data
python download_data.py

# Step 2: Clean data
python clean_data.py

# Step 3: Simulate payments and covenants
python simulate_data.py

# Step 4: Push to Airtable
python airtable_push.py

# Step 5: Run portfolio analysis
python covenant_check.py

# Step 6: Generate visualizations
python visualize.py

# Step 7: Generate investor report and action plan
python report_generator.py

# Step 8: Create Word document
python generate_docx.py
```

## Data Source
U.S. International Development Finance Corporation (DFC) — FY2024 Annual Project Data
https://www.dfc.gov/our-impact/transaction-data