---
title: "Market Analysis Report"
author: "Data Science Team"
date: "2024"
output_format: "html"
---

# Market Analysis Report

This example demonstrates Nhandu's advanced features with a simplified approach that avoids variable scoping issues.

## Setup and Data Generation

```python
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Try to import optional dependencies
try:
    import pandas as pd
    pandas_available = True
except ImportError:
    pandas_available = False

try:
    from sklearn.linear_model import LinearRegression
    sklearn_available = True
except ImportError:
    sklearn_available = False

# Set random seed for reproducibility
np.random.seed(42)

# Configuration
companies = ['TechCorp', 'DataSoft', 'CloudSys', 'InfoTech', 'DigitalPro']
regions = ['North', 'South', 'East', 'West', 'Central']
months = 24

print(f"Analyzing {len(companies)} companies across {len(regions)} regions over {months} months")
print(f"Pandas available: {pandas_available}")
print(f"Scikit-learn available: {sklearn_available}")
```

## Data Generation

```python
# Generate synthetic market data
all_data = []
base_date = datetime(2022, 1, 1)

for month in range(months):
    current_date = base_date + timedelta(days=30 * month)

    for company in companies:
        for region in regions:
            # Base performance with trends and seasonality
            base_performance = 100
            trend = month * 2  # Growth trend
            seasonal = 10 * np.sin(2 * np.pi * month / 12)  # Seasonal variation
            company_factor = np.random.normal(1, 0.1)
            region_factor = np.random.normal(1, 0.05)

            revenue = (base_performance + trend + seasonal) * company_factor * region_factor
            revenue += np.random.normal(0, 5)  # Add noise

            # Customer metrics
            customers = int(revenue * 0.8 + np.random.normal(0, 10))
            satisfaction = np.clip(np.random.normal(8.5, 1.2), 1, 10)

            all_data.append({
                'date': current_date,
                'month': month + 1,
                'company': company,
                'region': region,
                'revenue': max(0, revenue),
                'customers': max(0, customers),
                'satisfaction': satisfaction
            })

print(f"Generated {len(all_data)} records")
```

## Basic Analysis

```python
# Calculate basic statistics
all_revenues = [record['revenue'] for record in all_data]
all_satisfaction = [record['satisfaction'] for record in all_data]

print("\nBasic Statistics:")
print(f"Total revenue: ${sum(all_revenues):,.2f}k")
print(f"Average revenue: ${np.mean(all_revenues):,.2f}k")
print(f"Revenue std dev: ${np.std(all_revenues):,.2f}k")
print(f"Average satisfaction: {np.mean(all_satisfaction):.2f}")

# Calculate correlation
correlation = np.corrcoef(all_satisfaction, all_revenues)[0, 1]
print(f"Satisfaction-Revenue correlation: {correlation:.3f}")
```

## Company Analysis

```python
# Analyze by company
company_revenues = {}
for record in all_data:
    company = record['company']
    if company not in company_revenues:
        company_revenues[company] = []
    company_revenues[company].append(record['revenue'])

print("\nCompany Analysis:")
total_market = sum(all_revenues)
company_totals = {}
for company in companies:
    total_rev = sum(company_revenues[company])
    company_totals[company] = total_rev
    market_share = (total_rev / total_market) * 100
    avg_rev = np.mean(company_revenues[company])
    print(f"{company}: ${total_rev:,.0f}k total, {market_share:.1f}% share, ${avg_rev:.0f}k avg")

# Find top performer
best_company = max(company_totals, key=company_totals.get)
best_share = (company_totals[best_company] / total_market) * 100
print(f"\nTop performer: {best_company} with {best_share:.1f}% market share")
```

## Regional Analysis

```python
# Analyze by region
region_revenues = {}
for record in all_data:
    region = record['region']
    if region not in region_revenues:
        region_revenues[region] = []
    region_revenues[region].append(record['revenue'])

print("\nRegional Analysis:")
region_totals = {}
for region in regions:
    total_rev = sum(region_revenues[region])
    region_totals[region] = total_rev
    avg_rev = np.mean(region_revenues[region])
    print(f"{region}: ${total_rev:,.0f}k total, ${avg_rev:.0f}k avg")

best_region = max(region_totals, key=region_totals.get)
worst_region = min(region_totals, key=region_totals.get)
gap = region_totals[best_region] - region_totals[worst_region]
print(f"\nBest region: {best_region} (${region_totals[best_region]:,.0f}k)")
print(f"Gap with worst region: ${gap:,.0f}k")
```

## Trend Analysis

```python
# Monthly trend analysis
monthly_totals = {}
for record in all_data:
    month = record['month']
    if month not in monthly_totals:
        monthly_totals[month] = 0
    monthly_totals[month] += record['revenue']

months_list = sorted(monthly_totals.keys())
revenue_list = [monthly_totals[m] for m in months_list]

# Calculate growth rates
growth_rates = []
for i in range(1, len(revenue_list)):
    growth_rate = (revenue_list[i] - revenue_list[i-1]) / revenue_list[i-1] * 100
    growth_rates.append(growth_rate)

print("\nTrend Analysis:")
print(f"Average monthly growth rate: {np.mean(growth_rates):.2f}%")
print(f"Growth volatility: {np.std(growth_rates):.2f}%")

# Linear trend
X = np.array(months_list).reshape(-1, 1)
y = np.array(revenue_list)

# Simple linear regression
if sklearn_available:
    model = LinearRegression()
    model.fit(X, y)
    slope = model.coef_[0]
    r2 = model.score(X, y)
else:
    # Manual linear regression
    n = len(X)
    x_flat = X.flatten()
    slope = (n * np.sum(x_flat * y) - np.sum(x_flat) * np.sum(y)) / (n * np.sum(x_flat * x_flat) - np.sum(x_flat) * np.sum(x_flat))
    intercept = np.mean(y) - slope * np.mean(x_flat)
    y_pred = slope * x_flat + intercept
    r2 = 1 - np.sum((y - y_pred) ** 2) / np.sum((y - np.mean(y)) ** 2)

print(f"Monthly trend: ${slope:.2f}k per month")
print(f"R-squared: {r2:.4f}")
```

## Visualization

```python
# Create comprehensive visualization
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))

# 1. Monthly revenue trend
ax1.plot(months_list, revenue_list, 'b-', marker='o', linewidth=2)
ax1.set_title('Monthly Revenue Trend')
ax1.set_xlabel('Month')
ax1.set_ylabel('Revenue ($000s)')
ax1.grid(True, alpha=0.3)

# 2. Company comparison
company_names = list(company_totals.keys())
company_values = list(company_totals.values())
bars = ax2.bar(company_names, company_values, color='skyblue', edgecolor='navy')
ax2.set_title('Total Revenue by Company')
ax2.set_ylabel('Revenue ($000s)')
ax2.tick_params(axis='x', rotation=45)

# Add value labels
for bar, value in zip(bars, company_values):
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 50,
             f'${value:.0f}k', ha='center', va='bottom', fontsize=9)

# 3. Satisfaction vs Revenue scatter
ax3.scatter(all_satisfaction, all_revenues, alpha=0.6, s=20)
z = np.polyfit(all_satisfaction, all_revenues, 1)
p = np.poly1d(z)
ax3.plot(all_satisfaction, p(all_satisfaction), "r--", alpha=0.8, linewidth=2)
ax3.set_title(f'Satisfaction vs Revenue (r={correlation:.3f})')
ax3.set_xlabel('Customer Satisfaction')
ax3.set_ylabel('Revenue ($000s)')
ax3.grid(True, alpha=0.3)

# 4. Regional pie chart
region_names = list(region_totals.keys())
region_values = list(region_totals.values())
colors = plt.cm.Set3(np.linspace(0, 1, len(regions)))
ax4.pie(region_values, labels=region_names, autopct='%1.1f%%',
        colors=colors, startangle=90)
ax4.set_title('Revenue Distribution by Region')

plt.tight_layout()
plt.show()
```

## Summary and Recommendations

```python
# Generate summary
print("\n" + "="*50)
print("EXECUTIVE SUMMARY")
print("="*50)

print(f"Analysis of {len(all_data)} data points over {months} months:")
print(f"• Total market size: ${total_market:,.0f}k")
print(f"• Average monthly growth: {np.mean(growth_rates):.1f}%")
print(f"• Top performer: {best_company} ({best_share:.1f}% share)")
print(f"• Best region: {best_region}")
print(f"• Satisfaction correlation: {correlation:.3f}")

print(f"\nKey Recommendations:")
recommendations = []

if best_share > 25:
    recommendations.append(f"Monitor {best_company}'s market dominance")

if np.std(growth_rates) > 5:
    recommendations.append("High growth volatility suggests market opportunities")

if gap > 1000:
    recommendations.append(f"Focus expansion in {worst_region} region")

if correlation > 0.3:
    recommendations.append("Invest in customer satisfaction programs")

for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")

if not recommendations:
    print("1. Continue current strategy and monitor market trends")
```

## Technical Appendix

```python
print(f"\n" + "="*50)
print("TECHNICAL SPECIFICATIONS")
print("="*50)

start_date = min(record['date'] for record in all_data)
end_date = max(record['date'] for record in all_data)

print(f"Analysis Period: {start_date.strftime('%B %Y')} to {end_date.strftime('%B %Y')}")
print(f"Sample Size: {len(all_data):,} observations")
print(f"Features: Revenue, customers, satisfaction, company, region, temporal")
print(f"Dependencies: pandas={pandas_available}, sklearn={sklearn_available}")

print(f"\nReport generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

Try running: `nhandu examples/05_advanced_report_simple.md`