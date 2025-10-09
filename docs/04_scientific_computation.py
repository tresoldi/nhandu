#' ---
#' title: Scientific Computation with Nhandu
#' ---
#'
#' # Scientific Computation with Nhandu
#'
#' This example demonstrates more advanced scientific computing scenarios, including numerical methods, simulations, and mathematical analysis.
#'
#' ## Mathematical Functions and Numerical Methods

import numpy as np
import matplotlib.pyplot as plt
from math import factorial, pi, e

#' ### Numerical Integration: Estimating π
#'
#' Let's estimate π using Monte Carlo integration:

def estimate_pi(n_samples):
    """Estimate π using Monte Carlo method by sampling points in a unit square."""
    # Generate random points in [-1, 1] x [-1, 1]
    x = np.random.uniform(-1, 1, n_samples)
    y = np.random.uniform(-1, 1, n_samples)

    # Count points inside the unit circle
    inside_circle = (x**2 + y**2) <= 1
    pi_estimate = 4 * np.sum(inside_circle) / n_samples

    return pi_estimate, x, y, inside_circle

# Run simulation with different sample sizes
sample_sizes = [100, 1000, 10000, 100000]
estimates = []

print("Monte Carlo Estimation of π:")
print("Sample Size | Estimate | Error")
print("-" * 30)

for n in sample_sizes:
    pi_est, _, _, _ = estimate_pi(n)
    error = abs(pi_est - pi)
    estimates.append(pi_est)
    print(f"{n:10d} | {pi_est:.6f} | {error:.6f}")

print(f"\nActual π: {pi:.6f}")

#' ### Visualizing the Monte Carlo Method

# Create visualization for the largest sample
n_vis = 5000
pi_est, x_vis, y_vis, inside_vis = estimate_pi(n_vis)

plt.figure(figsize=(10, 10))
plt.scatter(x_vis[inside_vis], y_vis[inside_vis], c='red', s=1, alpha=0.6, label='Inside circle')
plt.scatter(x_vis[~inside_vis], y_vis[~inside_vis], c='blue', s=1, alpha=0.6, label='Outside circle')

# Draw the unit circle
theta = np.linspace(0, 2*pi, 100)
plt.plot(np.cos(theta), np.sin(theta), 'black', linewidth=2)

plt.xlim(-1.1, 1.1)
plt.ylim(-1.1, 1.1)
plt.gca().set_aspect('equal')
plt.title(f'Monte Carlo Estimation of π\n{n_vis} samples, estimate = {pi_est:.4f}')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

#' ## Differential Equations: Population Dynamics
#'
#' Let's model population growth with the logistic equation:

def logistic_growth(t, population, growth_rate=0.1, carrying_capacity=1000):
    """Logistic growth differential equation: dP/dt = r*P*(1 - P/K)"""
    return growth_rate * population * (1 - population / carrying_capacity)

def euler_method(func, y0, t_span, dt):
    """Simple Euler method for solving ODEs."""
    t_start, t_end = t_span
    t = np.arange(t_start, t_end + dt, dt)
    y = np.zeros(len(t))
    y[0] = y0

    for i in range(len(t) - 1):
        y[i + 1] = y[i] + dt * func(t[i], y[i])

    return t, y

# Solve the logistic equation
initial_population = 10
t_span = (0, 50)
dt = 0.1

time, population = euler_method(logistic_growth, initial_population, t_span, dt)

# Analytical solution for comparison
def logistic_analytical(t, P0=10, r=0.1, K=1000):
    return K / (1 + (K/P0 - 1) * np.exp(-r * t))

analytical_pop = logistic_analytical(time)

plt.figure(figsize=(12, 8))
plt.plot(time, population, 'b-', linewidth=2, label='Numerical (Euler method)')
plt.plot(time, analytical_pop, 'r--', linewidth=2, label='Analytical solution')
plt.axhline(y=1000, color='gray', linestyle=':', label='Carrying capacity')

plt.xlabel('Time')
plt.ylabel('Population')
plt.title('Logistic Population Growth Model')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Calculate and display final values
final_numerical = population[-1]
final_analytical = analytical_pop[-1]
print(f"Final population (numerical): {final_numerical:.2f}")
print(f"Final population (analytical): {final_analytical:.2f}")
print(f"Relative error: {abs(final_numerical - final_analytical)/final_analytical * 100:.4f}%")

#' ## Fourier Analysis: Signal Processing
#'
#' Let's analyze a composite signal using Fourier transforms:

# Create a composite signal
fs = 1000  # Sampling frequency
t = np.linspace(0, 2, fs * 2, endpoint=False)

# Composite signal: mix of sine waves with noise
freq1, freq2, freq3 = 50, 120, 200
signal = (np.sin(2 * pi * freq1 * t) +
          0.5 * np.sin(2 * pi * freq2 * t) +
          0.3 * np.sin(2 * pi * freq3 * t) +
          0.1 * np.random.randn(len(t)))

# Compute FFT
fft_signal = np.fft.fft(signal)
frequencies = np.fft.fftfreq(len(signal), 1/fs)

# Only take positive frequencies
positive_freq_idx = frequencies > 0
frequencies_pos = frequencies[positive_freq_idx]
fft_magnitude = np.abs(fft_signal[positive_freq_idx])

# Create subplots
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))

# Time domain signal
ax1.plot(t[:500], signal[:500])  # Show first 0.5 seconds
ax1.set_title('Time Domain Signal (first 0.5 seconds)')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Amplitude')
ax1.grid(True, alpha=0.3)

# Frequency domain (full spectrum)
ax2.plot(frequencies_pos, fft_magnitude)
ax2.set_title('Frequency Domain (FFT)')
ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Magnitude')
ax2.grid(True, alpha=0.3)

# Frequency domain (zoomed to relevant range)
freq_mask = frequencies_pos < 300
ax3.plot(frequencies_pos[freq_mask], fft_magnitude[freq_mask])
ax3.set_title('Frequency Domain (0-300 Hz)')
ax3.set_xlabel('Frequency (Hz)')
ax3.set_ylabel('Magnitude')
ax3.grid(True, alpha=0.3)

# Mark the expected frequencies
for freq in [freq1, freq2, freq3]:
    ax3.axvline(x=freq, color='red', linestyle='--', alpha=0.7,
                label=f'{freq} Hz' if freq == freq1 else "")

if freq1 == 50:  # Only add legend once
    ax3.legend()

plt.tight_layout()
plt.show()

# Find peaks in the frequency domain
peak_indices = []
peak_freqs = []
threshold = np.max(fft_magnitude) * 0.1  # 10% of maximum

for i in range(1, len(fft_magnitude) - 1):
    if (fft_magnitude[i] > fft_magnitude[i-1] and
        fft_magnitude[i] > fft_magnitude[i+1] and
        fft_magnitude[i] > threshold):
        peak_indices.append(i)
        peak_freqs.append(frequencies_pos[i])

print("Detected frequency components:")
for freq in sorted(peak_freqs):
    if freq < 300:  # Only show relevant frequencies
        print(f"  {freq:.1f} Hz")

print(f"\nExpected frequencies: {freq1}, {freq2}, {freq3} Hz")

#' ## Statistical Analysis: Hypothesis Testing
#'
#' Let's perform a statistical analysis comparing two datasets:

# Import scipy.stats for statistical testing
try:
    from scipy import stats
    scipy_available = True
except ImportError:
    print("Note: scipy not available - some statistical tests may be limited")
    scipy_available = False

# Generate two sample datasets
np.random.seed(42)
group_a = np.random.normal(100, 15, 50)  # Mean=100, std=15, n=50
group_b = np.random.normal(107, 18, 60)  # Mean=107, std=18, n=60

# Descriptive statistics
def describe_data(data, name):
    print(f"\n{name} Statistics:")
    print(f"  Sample size: {len(data)}")
    print(f"  Mean: {np.mean(data):.2f}")
    print(f"  Std Dev: {np.std(data, ddof=1):.2f}")
    print(f"  Median: {np.median(data):.2f}")
    print(f"  Min: {np.min(data):.2f}")
    print(f"  Max: {np.max(data):.2f}")

describe_data(group_a, "Group A")
describe_data(group_b, "Group B")

# Perform t-test (if scipy is available)
if scipy_available:
    t_stat, p_value = stats.ttest_ind(group_a, group_b)
    print(f"\nTwo-sample t-test:")
    print(f"  t-statistic: {t_stat:.4f}")
    print(f"  p-value: {p_value:.6f}")
    print(f"  Significant at α=0.05: {'Yes' if p_value < 0.05 else 'No'}")
else:
    print(f"\nBasic comparison (scipy not available):")
    print(f"  Group A mean: {np.mean(group_a):.2f}")
    print(f"  Group B mean: {np.mean(group_b):.2f}")
    print(f"  Mean difference: {np.mean(group_b) - np.mean(group_a):.2f}")

# Effect size (Cohen's d)
pooled_std = np.sqrt(((len(group_a)-1)*np.var(group_a, ddof=1) +
                     (len(group_b)-1)*np.var(group_b, ddof=1)) /
                    (len(group_a) + len(group_b) - 2))
cohens_d = (np.mean(group_b) - np.mean(group_a)) / pooled_std
print(f"  Cohen's d (effect size): {cohens_d:.4f}")

# Visualization
plt.figure(figsize=(14, 10))

# Histograms
plt.subplot(2, 2, 1)
plt.hist(group_a, bins=15, alpha=0.7, label='Group A', color='blue', density=True)
plt.hist(group_b, bins=15, alpha=0.7, label='Group B', color='red', density=True)
plt.xlabel('Value')
plt.ylabel('Density')
plt.title('Distribution Comparison')
plt.legend()
plt.grid(True, alpha=0.3)

# Box plots
plt.subplot(2, 2, 2)
plt.boxplot([group_a, group_b], labels=['Group A', 'Group B'])
plt.ylabel('Value')
plt.title('Box Plot Comparison')
plt.grid(True, alpha=0.3)

# Q-Q plots for normality check (if scipy available)
if scipy_available:
    plt.subplot(2, 2, 3)
    stats.probplot(group_a, dist="norm", plot=plt)
    plt.title('Q-Q Plot: Group A')
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 4)
    stats.probplot(group_b, dist="norm", plot=plt)
    plt.title('Q-Q Plot: Group B')
    plt.grid(True, alpha=0.3)
else:
    # Simple normality visualization without scipy
    plt.subplot(2, 2, 3)
    plt.hist(group_a, bins=15, alpha=0.7, density=True, color='blue')
    plt.title('Group A Distribution')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.grid(True, alpha=0.3)

    plt.subplot(2, 2, 4)
    plt.hist(group_b, bins=15, alpha=0.7, density=True, color='red')
    plt.title('Group B Distribution')
    plt.xlabel('Value')
    plt.ylabel('Density')
    plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

#' ## Summary
#'
#' This example demonstrates Nhandu's capability for scientific computing:
#'
#' - **Numerical methods**: Monte Carlo simulation for π estimation
#' - **Differential equations**: Population dynamics modeling with Euler method
#' - **Signal processing**: Fourier analysis of composite signals
#' - **Statistical analysis**: Hypothesis testing and effect size calculation
#'
#' Each section combines mathematical theory with practical implementation, showing how Nhandu can be used for educational content, research reports, or analysis documentation.
#'
#' Try running: `nhandu examples/04_scientific_computation.py`