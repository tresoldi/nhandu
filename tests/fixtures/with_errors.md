# Document with Errors

This document tests error handling.

```python
print("This works fine")
result = 1 + 1
print(f"1 + 1 = {result}")
```

This code block will have an error:

```python
undefined_variable = some_undefined_var
print("This won't print")
```

But execution should continue:

```python
print("This should still execute after the error")
x = "Error recovery works!"
x
```