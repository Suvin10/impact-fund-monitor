import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ── Load portfolio summary ─────────────────────────────────
with open("portfolio_summary.json", "r") as f:
    summary = json.load(f)

# ── Build prompt ───────────────────────────────────────────
breach_list = "\n".join([
    f"  - {b['borrower_name']} ({b['country']}): DSCR={b['dscr']}, D/E={b['debt_to_equity']}"
    for b in summary['breach_details'][:10]
])

missed_list = "\n".join([
    f"  - {m['borrower_name']} ({m['country']}): ${m['amount_due']:,.0f} missed"
    for m in summary['missed_details'][:10]
])

prompt = f"""
You are a senior portfolio analyst at an impact debt fund with $100M AUM.
Write a professional monthly investor report for May 2026 based on this data:

PORTFOLIO METRICS:
- Total Loans: {summary['total_loans']}
- Total AUM: ${summary['total_aum_usd']:,.0f}
- Collection Rate: {summary['collection_rate']}%
- On-Time Payment Rate: {summary['on_time_pct']}%
- Covenant Breaches: {summary['covenant_breaches']} loans
- Missed Payments: {summary['missed_payments']} instances
- Portfolio Health Score: {summary['health_score']}/100

TOP COVENANT BREACHES (DSCR < 1.25 or D/E > 3.0):
{breach_list}

TOP MISSED PAYMENTS:
{missed_list}

Write a 3-section report:
1. Executive Summary (2-3 sentences, overall portfolio health)
2. Key Risks & Action Items (bullet points, specific borrowers)
3. Outlook (forward looking, what the team will do next month)

Tone: Professional, concise, factual. Written for sophisticated investors.
"""

# ── Generate report ────────────────────────────────────────
print("Generating investor report with Groq...\n")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": prompt}],
    max_tokens=1000
)

report = response.choices[0].message.content

print("=" * 60)
print("IMPACT FUND PORTFOLIO — MONTHLY INVESTOR REPORT")
print("May 2026")
print("=" * 60)
print(report)

# ── Save report ────────────────────────────────────────────
with open("investor_report_may2026.txt", "w", encoding="utf-8") as f:
    f.write("IMPACT FUND PORTFOLIO — MONTHLY INVESTOR REPORT\n")
    f.write("May 2026\n")
    f.write("=" * 60 + "\n")
    f.write(report)

print("\nReport saved to investor_report_may2026.txt")


# ── Generate Action Items File ─────────────────────────────
action_prompt = f"""
Based on this impact fund portfolio data for May 2026:

- Portfolio Health Score: {summary['health_score']}/100
- Collection Rate: {summary['collection_rate']}%
- Covenant Breaches: {summary['covenant_breaches']} loans
- Missed Payments: {summary['missed_payments']} instances

TOP COVENANT BREACHES:
{breach_list}

TOP MISSED PAYMENTS:
{missed_list}

Generate a clear action plan for the fund manager with:
1. IMMEDIATE ACTIONS (this week) — specific borrowers to call, amounts at risk
2. SHORT TERM (this month) — restructuring candidates, covenant waivers to consider
3. WATCH LIST — borderline borrowers to monitor closely next month

Be specific with borrower names, amounts, and recommended actions.
Format as a practical decision-making guide, not a report.
"""

print("\nGenerating action plan...\n")

action_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": action_prompt}],
    max_tokens=1000
)

action_plan = action_response.choices[0].message.content

print("=" * 60)
print("FUND MANAGER ACTION PLAN — May 2026")
print("=" * 60)
print(action_plan)

# ── Save action plan ───────────────────────────────────────
with open("action_plan_may2026.txt", "w", encoding="utf-8") as f:
    f.write("FUND MANAGER ACTION PLAN — May 2026\n")
    f.write("=" * 60 + "\n")
    f.write(action_plan)

print("\nAction plan saved to action_plan_may2026.txt")