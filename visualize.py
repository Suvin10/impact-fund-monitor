import pandas as pd
import matplotlib.pyplot as plt
import json
import os

# ── Load data ──────────────────────────────────────────────
portfolio = pd.read_csv("portfolio_clean.csv")
payments  = pd.read_csv("payments.csv")
covenants = pd.read_csv("covenants.csv")

with open("portfolio_summary.json", "r") as f:
    summary = json.load(f)

os.makedirs("charts", exist_ok=True)

# ── Chart 1: Payment Status Distribution ──────────────────
fig, ax = plt.subplots(figsize=(7, 5))
payment_counts = payments['payment_status'].value_counts()
colors = ['#2ecc71', '#f39c12', '#e74c3c']
ax.pie(payment_counts, labels=payment_counts.index,
       autopct='%1.1f%%', colors=colors, startangle=90)
ax.set_title('Payment Status Distribution\nMay 2026', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/payment_status.png", dpi=150)
plt.close()
print("Chart 1 saved: payment_status.png")

# ── Chart 2: Loans by Sector ───────────────────────────────
fig, ax = plt.subplots(figsize=(9, 5))
sector_counts = portfolio['sector'].value_counts()
bars = ax.barh(sector_counts.index, sector_counts.values,
               color=['#3498db', '#2ecc71', '#9b59b6', '#e67e22'])
ax.set_xlabel('Number of Loans')
ax.set_title('Portfolio by Sector', fontsize=14, fontweight='bold')
for bar, val in zip(bars, sector_counts.values):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            str(val), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig("charts/loans_by_sector.png", dpi=150)
plt.close()
print("Chart 2 saved: loans_by_sector.png")

# ── Chart 3: Loans by Country (Top 10) ────────────────────
fig, ax = plt.subplots(figsize=(9, 6))
country_counts = portfolio['country'].value_counts().head(10)
bars = ax.barh(country_counts.index, country_counts.values, color='#3498db')
ax.set_xlabel('Number of Loans')
ax.set_title('Top 10 Countries by Loan Count', fontsize=14, fontweight='bold')
for bar, val in zip(bars, country_counts.values):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            str(val), va='center', fontweight='bold')
plt.tight_layout()
plt.savefig("charts/loans_by_country.png", dpi=150)
plt.close()
print("Chart 3 saved: loans_by_country.png")

# ── Chart 4: Covenant Status ───────────────────────────────
fig, ax = plt.subplots(figsize=(7, 5))
cov_counts = covenants['covenant_status'].value_counts()
colors = ['#2ecc71', '#e74c3c']
ax.pie(cov_counts, labels=cov_counts.index,
       autopct='%1.1f%%', colors=colors, startangle=90)
ax.set_title('Covenant Compliance Status\nMay 2026', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig("charts/covenant_status.png", dpi=150)
plt.close()
print("Chart 4 saved: covenant_status.png")

# ── Chart 5: Portfolio Health Score ───────────────────────
fig, ax = plt.subplots(figsize=(7, 4))
metrics = ['Collection Rate', 'On-Time Payments', 'Covenant Compliance', 'Health Score']
values  = [
    summary['collection_rate'],
    summary['on_time_pct'],
    round((180/243)*100, 1),
    summary['health_score']
]
colors = ['#2ecc71' if v >= 80 else '#f39c12' if v >= 60 else '#e74c3c' for v in values]
bars = ax.bar(metrics, values, color=colors)
ax.set_ylim(0, 110)
ax.axhline(y=80, color='green', linestyle='--', alpha=0.5, label='Healthy threshold (80)')
ax.set_ylabel('Score / Percentage')
ax.set_title('Portfolio Health Metrics — May 2026', fontsize=14, fontweight='bold')
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'{val}%', ha='center', fontweight='bold')
ax.legend()
plt.tight_layout()
plt.savefig("charts/health_metrics.png", dpi=150)
plt.close()
print("Chart 5 saved: health_metrics.png")

print("\nAll charts saved to /charts folder!")