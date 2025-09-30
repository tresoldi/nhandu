# Data Visualization with Nhandu

This example demonstrates how Nhandu captures and displays matplotlib plots alongside code and analysis.

## Setup

```python
import matplotlib.pyplot as plt
import numpy as np
import math

# Set up some sample data
np.random.seed(42)  # For reproducible results
```

## Simple Line Plot

Let's start with a basic line plot:

```python
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, 'b-', linewidth=2, label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Simple Sine Wave')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()
```

## Multiple Series

```python
x = np.linspace(0, 4*np.pi, 100)
y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.sin(x) * np.exp(-x/10)

plt.figure(figsize=(12, 8))
plt.plot(x, y1, 'b-', label='sin(x)', linewidth=2)
plt.plot(x, y2, 'r--', label='cos(x)', linewidth=2)
plt.plot(x, y3, 'g:', label='sin(x) * exp(-x/10)', linewidth=2)

plt.xlabel('x')
plt.ylabel('y')
plt.title('Multiple Trigonometric Functions')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## Scatter Plot with Analysis

Let's generate some sample data and create a scatter plot:

```python
# Generate sample data with some correlation
n_points = 100
x_data = np.random.normal(0, 1, n_points)
y_data = 2.5 * x_data + np.random.normal(0, 0.5, n_points) + 1

# Calculate correlation
correlation = np.corrcoef(x_data, y_data)[0, 1]
print(f"Correlation coefficient: {correlation:.3f}")

# Create scatter plot
plt.figure(figsize=(10, 8))
plt.scatter(x_data, y_data, alpha=0.6, s=50)

# Add trend line
z = np.polyfit(x_data, y_data, 1)
p = np.poly1d(z)
plt.plot(x_data, p(x_data), "r--", alpha=0.8, linewidth=2, label=f'Trend line (r={correlation:.3f})')

plt.xlabel('X values')
plt.ylabel('Y values')
plt.title('Scatter Plot with Trend Line')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
```

## Histogram

```python
# Generate sample data from different distributions
data1 = np.random.normal(0, 1, 1000)
data2 = np.random.normal(2, 1.5, 1000)

plt.figure(figsize=(12, 6))

# Create subplots
plt.subplot(1, 2, 1)
plt.hist(data1, bins=30, alpha=0.7, color='blue', edgecolor='black')
plt.title('Normal Distribution (μ=0, σ=1)')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.subplot(1, 2, 2)
plt.hist(data2, bins=30, alpha=0.7, color='red', edgecolor='black')
plt.title('Normal Distribution (μ=2, σ=1.5)')
plt.xlabel('Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()
```

## Bar Chart with Custom Styling

```python
# Sample data for bar chart
categories = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
sales = [234, 187, 312, 98, 267]
profits = [45, 23, 78, 12, 56]

x_pos = np.arange(len(categories))

plt.figure(figsize=(12, 8))

# Create grouped bar chart
width = 0.35
plt.bar(x_pos - width/2, sales, width, label='Sales', color='skyblue', edgecolor='navy')
plt.bar(x_pos + width/2, profits, width, label='Profits', color='lightcoral', edgecolor='darkred')

plt.xlabel('Products')
plt.ylabel('Amount ($000)')
plt.title('Sales and Profits by Product')
plt.xticks(x_pos, categories)
plt.legend()

# Add value labels on bars
for i, (sale, profit) in enumerate(zip(sales, profits)):
    plt.text(i - width/2, sale + 5, str(sale), ha='center', va='bottom')
    plt.text(i + width/2, profit + 2, str(profit), ha='center', va='bottom')

plt.grid(True, alpha=0.3, axis='y')
plt.show()
```

## Subplots with Different Chart Types

```python
# Create a 2x2 subplot layout
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))

# Plot 1: Line plot
x = np.linspace(0, 2*np.pi, 50)
ax1.plot(x, np.sin(x), 'b-', linewidth=2)
ax1.set_title('Sine Wave')
ax1.grid(True, alpha=0.3)

# Plot 2: Scatter plot
x_scatter = np.random.randn(50)
y_scatter = 2 * x_scatter + np.random.randn(50)
ax2.scatter(x_scatter, y_scatter, alpha=0.6)
ax2.set_title('Random Scatter Plot')
ax2.grid(True, alpha=0.3)

# Plot 3: Bar chart
categories = ['A', 'B', 'C', 'D']
values = [23, 17, 35, 29]
ax3.bar(categories, values, color=['red', 'green', 'blue', 'orange'])
ax3.set_title('Bar Chart')

# Plot 4: Pie chart
sizes = [30, 25, 20, 25]
labels = ['Segment 1', 'Segment 2', 'Segment 3', 'Segment 4']
ax4.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax4.set_title('Pie Chart')

plt.tight_layout()
plt.show()
```

## Statistical Summary

Let's print some statistics about our data:

```python
print("Data Analysis Summary:")
print(f"Correlation between x_data and y_data: {correlation:.3f}")
print(f"Mean of data1: {np.mean(data1):.3f}")
print(f"Standard deviation of data1: {np.std(data1):.3f}")
print(f"Mean of data2: {np.mean(data2):.3f}")
print(f"Standard deviation of data2: {np.std(data2):.3f}")
print(f"Total sales: ${sum(sales)}k")
print(f"Total profits: ${sum(profits)}k")
print(f"Average profit margin: {(sum(profits)/sum(sales))*100:.1f}%")
```

## Conclusion

This example demonstrates Nhandu's ability to:
- Capture matplotlib plots automatically
- Display multiple plots in a single document
- Combine visualizations with data analysis
- Create comprehensive reports with code, plots, and results

The plots will be embedded directly in the output HTML, making it perfect for sharing analysis results.

Try running: `nhandu examples/03_plotting.md`