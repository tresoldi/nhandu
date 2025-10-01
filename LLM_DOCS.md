---
document_type: llm_guide
target_audience: coding_agents
library: nhandu
version: 0.1.0
purpose: Guide for AI coding assistants to generate literate Python programs using Nhandu
---

# Nhandu Guide for AI Coding Assistants

This document provides comprehensive guidance for AI coding assistants (LLMs, coding agents) on how to help users create literate Python programs using Nhandu.

## What is Nhandu?

Nhandu is a literate programming tool for Python that transforms ordinary `.py` files with markdown comments into beautiful HTML reports. It executes code blocks sequentially, captures output (print statements, plots, expression results), and weaves them together with documentation.

**Target Use Case:** Scientific computing, data analysis, reproducible research, and technical documentation where code and narrative need to be tightly integrated.

## Core Syntax Reference

### Markdown Comments

Lines starting with `#'` (hash + apostrophe + space) are treated as **markdown documentation**:

```python
#' # This is a Level 1 Heading
#'
#' This is a paragraph of markdown text. You can use **bold**, *italic*,
#' `code`, and all standard markdown features.
#'
#' ## This is a Level 2 Heading
#'
#' - Bullet point 1
#' - Bullet point 2
```

**Critical Rules:**
- ✅ Must have a space after `#'` → `#' Text here`
- ❌ No space = not recognized → `#'Text here` (wrong)
- ✅ Empty markdown lines need just `#'` → blank documentation line
- ✅ All standard markdown syntax works (headings, lists, links, tables, code blocks)

### Regular Python Code

Any line that does NOT start with `#'` is **executable Python code**:

```python
#' Let's do some calculations:

x = 42
y = x * 2
print(f"The result is {y}")

#' The variables persist across blocks.
```

**Key Points:**
- Regular Python comments with `#` work normally (they're code comments, not documentation)
- Code blocks are executed in document order
- All code shares the same Python namespace (variables persist)
- Expression results are captured (like Jupyter cells)

### Hidden Code Blocks

Use `#| hide` and `#|` to create code blocks that **execute but don't appear** in the output:

```python
#' # My Analysis Report

#| hide
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Setup code, imports, configuration
plt.style.use('seaborn-v0_8')
#|

#' Now let's analyze the data:

# This code WILL appear in the output
data = pd.read_csv('data.csv')
print(data.head())
```

**When to Use Hidden Blocks:**
- ✅ Import statements (keeps report clean)
- ✅ Configuration code (plot styles, pandas options)
- ✅ Helper function definitions
- ✅ Data loading boilerplate
- ❌ Don't hide the actual analysis (defeats the purpose of literate programming)

## Execution Model

### How Code Executes

1. **Shared Namespace:** All code blocks share the same Python environment
2. **Sequential Execution:** Blocks execute in document order (top to bottom)
3. **State Persistence:** Variables defined in one block are available in all subsequent blocks

```python
#' First block:
x = 10

#' Second block:
y = x + 5  # x is still available
print(y)   # Outputs: 15
```

### Output Capture

Nhandu automatically captures:

1. **Print statements and stdout:**
   ```python
   print("This will appear in the output")
   ```

2. **Expression results** (last expression in a block, like Jupyter):
   ```python
   2 + 2  # Will display: 4
   ```

3. **Matplotlib figures** (automatically, no `plt.show()` needed):
   ```python
   plt.plot([1, 2, 3], [1, 4, 9])
   plt.title("My Plot")
   # Figure captured automatically, embedded in HTML
   ```

4. **Rich objects** (pandas DataFrames render as HTML tables):
   ```python
   df.head()  # Renders as a nice table in HTML output
   ```

## Common Patterns for Coding Assistants

### Pattern 1: Data Analysis Report

```python
#' # Sales Analysis Report
#'
#' This report analyzes Q1 2024 sales data to identify trends and opportunities.

#| hide
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#|

#' ## Data Loading
#'
#' First, let's load the sales data:

df = pd.read_csv('sales_q1_2024.csv')
print(f"Loaded {len(df)} records")
df.head()

#' ## Summary Statistics

print("Sales Overview:")
print(f"Total Revenue: ${df['revenue'].sum():,.2f}")
print(f"Average Order Value: ${df['revenue'].mean():.2f}")
print(f"Number of Customers: {df['customer_id'].nunique()}")

#' ## Visualization

plt.figure(figsize=(10, 6))
df.groupby('month')['revenue'].sum().plot(kind='bar')
plt.title('Revenue by Month')
plt.ylabel('Revenue ($)')
plt.xlabel('Month')

#' ## Conclusions
#'
#' Key findings:
#' - Revenue peaked in March
#' - Average order value increased 15% quarter-over-quarter
```

### Pattern 2: Scientific Computation

```python
#' # Numerical Methods: Newton's Method
#'
#' Demonstrating Newton's method for finding roots of equations.

#| hide
import numpy as np
import matplotlib.pyplot as plt
#|

#' ## Problem Setup
#'
#' We want to find the root of $f(x) = x^2 - 2$ (i.e., find $\sqrt{2}$).

def f(x):
    return x**2 - 2

def df(x):
    return 2*x

#' ## Implementation

def newtons_method(f, df, x0, tol=1e-6, max_iter=100):
    """Apply Newton's method to find root."""
    x = x0
    for i in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x, i+1
        x = x - fx / df(x)
    return x, max_iter

root, iterations = newtons_method(f, df, x0=1.0)
print(f"Root found: {root:.10f}")
print(f"Actual √2:  {np.sqrt(2):.10f}")
print(f"Iterations: {iterations}")

#' ## Visualization

x = np.linspace(-1, 3, 100)
plt.figure(figsize=(10, 6))
plt.plot(x, f(x), label='f(x) = x² - 2')
plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
plt.axvline(x=root, color='r', linestyle='--', alpha=0.5, label=f'Root: {root:.4f}')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title("Newton's Method Result")
plt.legend()
plt.grid(True, alpha=0.3)
```

### Pattern 3: Tutorial/Educational Content

```python
#' # Introduction to List Comprehensions
#'
#' This tutorial demonstrates Python list comprehensions with practical examples.
#'
#' ## Basic Syntax
#'
#' The general form is: `[expression for item in iterable]`

# Example: squares of numbers 0-9
squares = [x**2 for x in range(10)]
print(squares)

#' ## With Conditions
#'
#' You can add a condition: `[expression for item in iterable if condition]`

# Example: even squares only
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)

#' ## Nested Comprehensions

# Create a multiplication table
table = [[i*j for j in range(1, 6)] for i in range(1, 6)]
for row in table:
    print(row)

#' ## Performance Comparison

#| hide
import time
#|

# Compare comprehension vs loop
n = 1000000

start = time.time()
result1 = [x**2 for x in range(n)]
time1 = time.time() - start

start = time.time()
result2 = []
for x in range(n):
    result2.append(x**2)
time2 = time.time() - start

print(f"List comprehension: {time1:.4f}s")
print(f"Traditional loop:   {time2:.4f}s")
print(f"Speedup: {time2/time1:.2f}x")
```

## Do's and Don'ts

### ✅ DO:

1. **Use hidden blocks for imports:**
   ```python
   #| hide
   import pandas as pd
   import matplotlib.pyplot as plt
   #|
   ```

2. **Structure documents with markdown headings:**
   ```python
   #' # Main Title
   #' ## Section
   #' ### Subsection
   ```

3. **Let matplotlib figures be captured automatically:**
   ```python
   plt.plot([1, 2, 3], [1, 4, 9])
   plt.title("My Plot")
   # No plt.show() needed!
   ```

4. **Use print() for narrative output:**
   ```python
   print(f"Analysis complete: {len(data)} records processed")
   ```

5. **Leverage expression results:**
   ```python
   df.describe()  # Last expression displays automatically
   ```

### ❌ DON'T:

1. **Forget the space after `#'`:**
   ```python
   #'This won't work  # ❌ Missing space
   #' This works      # ✅ Correct
   ```

2. **Call `plt.show()` explicitly:**
   ```python
   plt.plot(x, y)
   plt.show()  # ❌ Not needed, will cause issues
   ```

3. **Hide important analysis code:**
   ```python
   #| hide
   # Don't hide the actual analysis!
   result = perform_key_analysis(data)
   #|
   ```

4. **Rely on code comments for documentation:**
   ```python
   # This is just a code comment, won't appear in doc
   #' Use markdown comments for documentation
   ```

5. **Mix up regular `#` with `#'`:**
   ```python
   # This is a code comment (stays in code block)
   #' This is documentation (rendered as markdown)
   ```

## Compiling to HTML

### Basic Command

```bash
nhandu document.py
```

This creates `document.html` with your code, output, and documentation.

### Common Options

```bash
# Specify output file
nhandu analysis.py -o report.html

# Output as markdown instead of HTML
nhandu analysis.py --format md

# Use a different syntax highlighting theme
nhandu analysis.py --code-theme monokai

# Show processing details
nhandu analysis.py --verbose

# Use a configuration file
nhandu analysis.py --config config.yaml
```

### Configuration via YAML Frontmatter

Add configuration to the top of your `.py` file:

```python
#' ---
#' title: My Scientific Report
#' output: html
#' code_theme: dracula
#' plot_dpi: 150
#' ---
#'
#' # Introduction
#' ...
```

## Error Prevention Checklist

When generating literate Python files, ensure:

- [ ] All markdown lines start with `#' ` (with space)
- [ ] Hidden blocks are properly closed: `#| hide` ... `#|`
- [ ] No `plt.show()` calls (automatic capture)
- [ ] Imports are in hidden blocks (keeps output clean)
- [ ] Code blocks are in logical order (sequential execution)
- [ ] Variables are defined before use
- [ ] Clear section headings using `#'` markdown syntax
- [ ] Documentation explains *why*, not just *what* the code does

## Quick Reference Card

| Element | Syntax | Example |
|---------|--------|---------|
| Markdown text | `#' text` | `#' This is **bold** text` |
| Heading | `#' # Title` | `#' ## Section 2.1` |
| Code block | Regular Python | `x = 42` |
| Hidden code | `#\| hide` ... `#\|` | See examples above |
| Code comment | `#` | `# This is a code comment` |
| List | `#' - item` | `#' 1. First item` |
| Math | `#' $equation$` | `#' $E = mc^2$` |

## Output Formats

- **HTML** (default): Self-contained file with embedded plots, syntax highlighting
- **Markdown**: Plain markdown with figure links (can be converted to PDF/Word with pandoc)

## Summary for Coding Assistants

When a user asks you to create a literate Python program or Nhandu document:

1. Start with a clear title and introduction using `#'` markdown
2. Hide imports and setup code with `#| hide` ... `#|`
3. Structure the document with markdown headings
4. Alternate between documentation (`#'`) and code blocks
5. Let the narrative explain the *why* and *context*
6. Let the code show the *how* and *implementation*
7. Use `print()` for key results and insights
8. Create visualizations without `plt.show()`
9. End with conclusions or next steps
10. Tell users to compile with: `nhandu filename.py`

