# Impact Fund Portfolio Monitor

A end-to-end portfolio monitoring system for an impact debt fund, built with Python, Airtable, and AI.

## What It Does
- Downloads real U.S. DFC impact loan portfolio data (1,300+ loans)
- Cleans and filters to 243 relevant Asia/Africa loans
- Simulates monthly payment tracking and covenant compliance checks
- Pushes all data to Airtable for live monitoring
- Runs automated portfolio health analysis
- Uses AI (Groq/LLaMA) to auto-generate monthly investor reports

## Portfolio Health Output
- Collection Rate: 92.6%
- On-Time Payment Rate: 80.0%
- Covenant Breaches: 63 loans flagged
- Portfolio Health Score: 77/100 (WATCH status)

## Tech Stack
- Python (pandas, requests)
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
| covenant_check.py | Live analysis - flags breaches and missed payments |
| report_generator.py | AI generates monthly investor report |

## Data Source
U.S. International Development Finance Corporation (DFC) - FY2024 Annual Project Data
https://www.dfc.gov/our-impact/transaction-data