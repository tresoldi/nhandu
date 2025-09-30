# Document with Matplotlib Plots

This document tests plot generation.

```python
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, label='sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sine Wave')
plt.legend()
plt.grid(True)
```

Another plot:

```python
x2 = np.linspace(0, 10, 50)
y2 = np.exp(-x2/5) * np.cos(x2)

plt.figure(figsize=(6, 4))
plt.plot(x2, y2, 'r-', linewidth=2)
plt.title('Damped Oscillation')
plt.xlabel('Time')
plt.ylabel('Amplitude')
```