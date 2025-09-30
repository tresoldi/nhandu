# Document with Hidden Blocks

This document tests hidden code blocks.

```python {hide=true}
# This block should not appear in output
secret_data = "This is hidden"
hidden_result = 42 * 2
```

```python
# This block is visible
print("This is visible")
print(f"Hidden result was: {hidden_result}")
```

Another hidden block:

```python {hidden}
# Alternative hidden syntax
another_secret = "Also hidden"
```

Final visible block:

```python
print("Final block")
if 'another_secret' in locals():
    print("Hidden block executed successfully")
```