#' # Data Analysis with Nhandu
#'
#' This example demonstrates basic data analysis capabilities using Python's built-in libraries and common data science patterns.
#'
#' ## Sample Dataset
#'
#' Let's create a simple dataset to work with:

#| hide
import csv
import io
from collections import Counter
import statistics
#|

# Create sample sales data
sales_data = [
    ["Date", "Product", "Category", "Sales", "Profit"],
    ["2024-01-01", "Laptop", "Electronics", 1200, 300],
    ["2024-01-02", "Book", "Education", 25, 10],
    ["2024-01-03", "Phone", "Electronics", 800, 200],
    ["2024-01-04", "Chair", "Furniture", 150, 50],
    ["2024-01-05", "Laptop", "Electronics", 1200, 300],
    ["2024-01-06", "Desk", "Furniture", 300, 100],
    ["2024-01-07", "Book", "Education", 25, 10],
    ["2024-01-08", "Phone", "Electronics", 800, 200],
]

print(f"Created dataset with {len(sales_data)-1} sales records")

#' ## Data Processing
#'
#' Let's analyze this data using Python's standard library:

# Extract headers and data
headers = sales_data[0]
data = sales_data[1:]

print("Headers:", headers)
print(f"Sample record: {data[0]}")

#' ## Sales Analysis
#'
#' ### Total Sales and Profit

total_sales = sum(float(row[3]) for row in data)
total_profit = sum(float(row[4]) for row in data)

print(f"Total Sales: ${total_sales:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
print(f"Profit Margin: {(total_profit/total_sales)*100:.1f}%")

#' ### Sales by Category

category_sales = {}
category_profit = {}

for row in data:
    category = row[2]
    sales = float(row[3])
    profit = float(row[4])

    category_sales[category] = category_sales.get(category, 0) + sales
    category_profit[category] = category_profit.get(category, 0) + profit

print("Sales by Category:")
for category in sorted(category_sales.keys()):
    sales = category_sales[category]
    profit = category_profit[category]
    margin = (profit/sales)*100
    print(f"  {category}: ${sales:,.2f} (${profit:,.2f} profit, {margin:.1f}% margin)")

#' ### Product Performance

product_counter = Counter(row[1] for row in data)
print("\nProduct Sales Frequency:")
for product, count in product_counter.most_common():
    print(f"  {product}: {count} sales")

#' ## Statistical Summary

sales_values = [float(row[3]) for row in data]
profit_values = [float(row[4]) for row in data]

print("\nSales Statistics:")
print(f"  Mean: ${statistics.mean(sales_values):.2f}")
print(f"  Median: ${statistics.median(sales_values):.2f}")
print(f"  Min: ${min(sales_values):.2f}")
print(f"  Max: ${max(sales_values):.2f}")
print(f"  Standard Deviation: ${statistics.stdev(sales_values):.2f}")

print("\nProfit Statistics:")
print(f"  Mean: ${statistics.mean(profit_values):.2f}")
print(f"  Median: ${statistics.median(profit_values):.2f}")
print(f"  Min: ${min(profit_values):.2f}")
print(f"  Max: ${max(profit_values):.2f}")

#' ## Simple Data Transformation
#'
#' Let's create a summary table:

# Create summary by category
summary = []
for category in sorted(category_sales.keys()):
    sales = category_sales[category]
    profit = category_profit[category]
    count = sum(1 for row in data if row[2] == category)
    avg_sale = sales / count

    summary.append([category, count, sales, profit, avg_sale])

# Display summary table
print("\nCategory Summary:")
print("Category      | Count | Total Sales | Total Profit | Avg Sale")
print("-" * 60)
for row in summary:
    print(f"{row[0]:<12} | {row[1]:5d} | ${row[2]:9.2f} | ${row[3]:10.2f} | ${row[4]:7.2f}")

#' ## Conclusion
#'
#' This example demonstrates:
#' - Working with structured data using Python's standard library
#' - Basic statistical calculations
#' - Data aggregation and grouping
#' - Simple reporting and formatting
#'
#' For more complex analysis, you'd typically use pandas, but this shows what's possible with just the standard library.
#'
#' Try running: `nhandu examples/02_data_analysis.py`