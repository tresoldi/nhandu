# Document with Inline Code

<% import datetime %>
This report was generated on <%= datetime.date.today() %>.

```python
x = 42
y = 24
```

The sum of <%= x %> and <%= y %> is <%= x + y %>.

<% z = x * y %>
The product (stored in z) is <%= z %>.