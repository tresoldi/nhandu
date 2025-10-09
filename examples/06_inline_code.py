#' ---
#' title: Inline Code Evaluation
#' ---
#'
#' # Inline Code Evaluation
#'
#' This example demonstrates Nhandu's inline code feature, which allows you to embed Python expressions and statements directly within markdown text.
#'
#' ## Basic Inline Expressions
#'
#' Use `<%= expression %>` to evaluate and display Python expressions within text:

#| hide
import datetime
import math
#|

#' The current date is <%= datetime.date.today() %>.
#'
#' Simple math: 2 + 2 = <%= 2 + 2 %>, and 10 × 15 = <%= 10 * 15 %>.
#'
#' You can also use Python's built-in functions: the square root of 144 is <%= math.sqrt(144) %>.

#' ## Inline Statements
#'
#' Use `<% statement %>` to execute code without displaying output:

#' <% greeting = "Hello, Nhandu!" %>
#' The greeting variable is now set to: <%= greeting %>

#' ## Working with Variables from Code Blocks
#'
#' Inline code shares the same namespace as regular code blocks:

# Define some variables
product_name = "Premium Widget"
price = 49.99
quantity = 150
discount_rate = 0.15

#' We have <%= quantity %> units of <%= product_name %> priced at $<%= price %> each.
#'
#' <% total_value = price * quantity %>
#' <% discounted_price = price * (1 - discount_rate) %>
#'
#' The total inventory value is $<%= f"{total_value:,.2f}" %>.
#' With a <%= discount_rate * 100 %>% discount, the price becomes $<%= f"{discounted_price:.2f}" %>.

#' ## Dynamic Report Generation
#'
#' Inline code is perfect for creating dynamic reports:

# Sales data
sales_q1 = 125000
sales_q2 = 148000
sales_q3 = 162000
sales_q4 = 189000

#' <% total_sales = sales_q1 + sales_q2 + sales_q3 + sales_q4 %>
#' <% avg_quarterly = total_sales / 4 %>
#' <% growth_rate = ((sales_q4 - sales_q1) / sales_q1) * 100 %>
#'
#' ### Annual Sales Summary
#'
#' - **Q1 Sales**: $<%= f"{sales_q1:,}" %>
#' - **Q2 Sales**: $<%= f"{sales_q2:,}" %>
#' - **Q3 Sales**: $<%= f"{sales_q3:,}" %>
#' - **Q4 Sales**: $<%= f"{sales_q4:,}" %>
#'
#' **Total Annual Sales**: $<%= f"{total_sales:,}" %>
#'
#' **Average Quarterly Sales**: $<%= f"{avg_quarterly:,.0f}" %>
#'
#' **Year-over-Year Growth**: <%= f"{growth_rate:.1f}" %>%

#' ## Conditional Text
#'
#' You can use inline code to generate conditional text:

# Performance metrics
target = 500000
actual = total_sales

#' <% performance = "exceeded" if actual > target else "fell short of" %>
#' <% status_icon = "✓" if actual > target else "✗" %>
#'
#' <%= status_icon %> We <%= performance %> our annual target of $<%= f"{target:,}" %>.

#' ## Scientific Calculations
#'
#' Inline code works well for presenting scientific results:

# Physics calculation
mass = 2.5  # kg
velocity = 15  # m/s

#' <% kinetic_energy = 0.5 * mass * velocity ** 2 %>
#'
#' An object with mass <%= mass %> kg moving at <%= velocity %> m/s has a kinetic energy of <%= f"{kinetic_energy:.1f}" %> joules.

# Circle calculations
radius = 7.5

#' <% area = math.pi * radius ** 2 %>
#' <% circumference = 2 * math.pi * radius %>
#'
#' A circle with radius <%= radius %> cm has:
#' - Area: <%= f"{area:.2f}" %> cm²
#' - Circumference: <%= f"{circumference:.2f}" %> cm

#' ## Complex Expressions
#'
#' You can use any Python expression, including list comprehensions:

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

#' The sum of numbers 1-10 is <%= sum(numbers) %>.
#'
#' The even numbers are: <%= ", ".join(str(n) for n in numbers if n % 2 == 0) %>.
#'
#' The squares of the first 5 numbers are: <%= [n**2 for n in numbers[:5]] %>.

#' ## Date and Time Examples
#'
#' Inline code is useful for timestamps and date calculations:

#' <% now = datetime.datetime.now() %>
#' <% next_week = now + datetime.timedelta(days=7) %>
#'
#' Current time: <%= now.strftime("%Y-%m-%d %H:%M:%S") %>
#'
#' One week from now: <%= next_week.strftime("%Y-%m-%d") %>
#'
#' Day of the week: <%= now.strftime("%A") %>

#' ## Formatting Numbers
#'
#' Python's formatting capabilities work seamlessly with inline code:

large_number = 1_234_567.89

#' - Default: <%= large_number %>
#' - With thousand separators: <%= f"{large_number:,}" %>
#' - Two decimal places: <%= f"{large_number:.2f}" %>
#' - Scientific notation: <%= f"{large_number:.2e}" %>

percentage = 0.847

#' - As decimal: <%= percentage %>
#' - As percentage: <%= f"{percentage:.1%}" %>

#' ## Best Practices
#'
#' **When to use inline code:**
#' - Embedding calculated values in narrative text
#' - Dynamic dates, timestamps, or metadata
#' - Simple conditional text
#' - Formatting and presenting results inline
#'
#' **When NOT to use inline code:**
#' - Complex logic (use regular code blocks instead)
#' - Code that needs to be visible for documentation
#' - Multi-line operations
#'
#' ## Conclusion
#'
#' Inline code evaluation makes your documents truly dynamic, allowing you to:
#' - Create data-driven narratives
#' - Generate reports with live calculations
#' - Embed timestamps and metadata automatically
#' - Present results naturally within prose
#'
#' Try running: `nhandu examples/06_inline_code.py`
