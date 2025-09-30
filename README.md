# Nhandu 

> *Nhandu* (ɲãndu, approximately "NYAN-doo") means "spider" in many Tupi-Guarani languages, a fitting name for a tool that weaves together code and documentation, much like Knuth's original vision of literate programming.

**Literate programming for Python: Write executable documents in plain `.py` files.**

Nhandu transforms ordinary Python files with markdown comments into beautiful, reproducible reports. It's lighter than Jupyter, simpler than Quarto, and perfectly git-friendly.

## Why Nhandu?

Contemporary literate programming in Python faces a documentation dilemma:

- **Jupyter notebooks** are powerful but use JSON format (git diffs are messy), require a browser/server, and mix code with metadata
- **Quarto** is feature-rich but complex, with many configuration options and a learning curve
- **Traditional scripts** lack integrated documentation and visualization

**Nhandu offers a better way:**

- Write literate programs in **normal `.py` files**: no special format, just comments
- **Perfect git diffs**: plain text, not JSON
- **No server or browser** required—just run the command
- **Zero configuration needed**: smart defaults get you started immediately
- **Python-native**: designed specifically for the Python ecosystem

Nhandu also supports traditional `.md` files with code blocks if you prefer that style.

## Quick Start

### Your First Literate Program

Create a file `analysis.py`:

```python
#' # My First Analysis
#'
#' This is a literate Python program. Lines starting with `#'` are markdown.
#' Everything else is regular Python code.

import numpy as np

# Generate some data
data = np.random.normal(0, 1, 1000)

#' ## Results
#'
#' Let's compute some statistics:

print(f"Mean: {data.mean():.3f}")
print(f"Std Dev: {data.std():.3f}")

#' The data looks normally distributed, as expected.
```

### Generate Your Report

```bash
nhandu analysis.py
```

This creates `analysis.html` with your code, output, and nicely formatted documentation, from a plain Python script.

## Features

### Smart Output Capture

Nhandu automatically captures:

- **Print statements** and stdout
- **Matplotlib plots** (no `plt.show()` needed!)
- **Expression results** (like Jupyter cells)
- **Rich objects** (DataFrames render as tables in HTML)

### Syntax Highlighting

Beautiful server-side syntax highlighting with 50+ themes via Pygments. Popular themes: `github-dark` (default), `monokai`, `dracula`, `one-dark`, `vs`, `solarized-light`

### Multiple Output Formats

**Note**: Markdown output can be converted to PDF, Word, LaTeX, and more using [pandoc](https://pandoc.org/) or similar tools. Native PDF support is planned.

### Configuration (Optional)

Power users can customize their reports via YAML frontmatter:

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

It is also possible to use a configuration file (`nhandu.yaml`) or CLI arguments.

## How It Works

### Literate Python Format (`.py` files)

Nhandu treats Python files specially when they contain markdown comments:

```python
#' # This is a markdown heading
#'
#' Any line starting with #' is treated as **markdown**.
#' You can use all standard markdown features.

# This is a regular Python comment
x = 42  # Regular code continues to work normally

#' Back to documentation. Variables persist across blocks:

print(f"x = {x}")
```

**Hidden code blocks** let you run setup code without cluttering your report:

```python
#| hide
import pandas as pd
import matplotlib.pyplot as plt
# Configuration code here—runs but doesn't appear in output
#|

#' Now let's analyze our data:
# This code WILL appear in the output
data = pd.read_csv("data.csv")
```

### Traditional Markdown Format (`.md` files)

You can also use standard markdown files with code blocks:

````markdown
# My Analysis

Here's some Python code:

```python
import numpy as np
x = np.linspace(0, 10, 100)
print(f"Generated {len(x)} points")
```

The output will appear in your rendered document. In case of HTML output, any figures are embedded in the file, so that you have a single file to distribute.

````

### Execution Model

- **Shared namespace**: All code blocks share the same Python environment
- **Sequential execution**: Blocks run in document order
- **Output capture**: stdout, plots, and expression results are all captured
- **Rich formatting**: Automatic handling of matplotlib figures, pandas DataFrames, and more

## Comparison with Other Tools

| Feature | Nhandu | Jupyter | Quarto | R Markdown | Pweave |
|---------|--------|---------|--------|------------|--------|
| **Format** | Plain `.py` or `.md` | JSON | Multiple | `.Rmd` | `.pmd` |
| **Git-friendly** | ✅ Perfect | ⚠️ Messy diffs | ✅ Good | ✅ Good | ✅ Good |
| **Complexity** | 🟢 Simple | 🟡 Medium | 🔴 Complex | 🟡 Medium | 🟢 Simple |
| **Python-native** | ✅ Yes | ✅ Yes | ⚠️ Multi-language | ❌ R-focused | ✅ Yes |
| **Requires server** | ❌ No | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Zero config** | ✅ Yes | ✅ Yes | ❌ No | ⚠️ Some | ⚠️ Some |
| **Active maintenance** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes | ❌ Unmaintained |

## Examples

Here's a complete example showing data analysis with visualization:

```python
#' # Sales Analysis Report
#'
#' This report analyzes Q1 sales data and identifies trends.

#| hide
import pandas as pd
import matplotlib.pyplot as plt
#|

#' ## Data Loading
#'
#' First, let's load our sales data:

data = pd.read_csv("sales.csv")
print(f"Loaded {len(data)} sales records")

#' ## Summary Statistics

print(data.describe())

#' ## Visualization

plt.figure(figsize=(10, 6))
data.groupby('month')['revenue'].sum().plot(kind='bar')
plt.title('Revenue by Month')
plt.ylabel('Revenue ($)')

#' The chart shows steady growth throughout Q1.
```

### More Examples

Check out the [`examples/`](examples/) directory for complete demonstrations:

- **[01_hello_world.py](examples/01_hello_world.py)** - Basic syntax and concepts
- **[02_data_analysis.py](examples/02_data_analysis.py)** - Working with data using standard library
- **[03_plotting.py](examples/03_plotting.py)** - Creating visualizations with matplotlib
- **[04_scientific_computation.py](examples/04_scientific_computation.py)** - Numerical computing with NumPy
- **[05_advanced_report.py](examples/05_advanced_report.py)** - Complex report with pandas and multiple visualizations

## Installation & Usage

### Install from PyPI

```bash
pip install nhandu
```

### Install from Source

```bash
git clone https://github.com/tresoldi/nhandu.git
cd nhandu
pip install -e .
```

### Basic Usage

```bash
nhandu document.py              # Process literate Python file → document.html
nhandu document.md              # Process markdown file → document.html
nhandu document.py -o report.html  # Specify output file
nhandu document.py --format md     # Output as markdown
nhandu document.py --code-theme monokai  # Custom syntax theme
nhandu document.py --verbose       # Show processing details
```

### CLI Options

```
nhandu [OPTIONS] INPUT

Options:
  -o, --output PATH           Output file path
  --format {html,md}          Output format (default: html)
  --config PATH               Configuration file (YAML)
  --working-dir PATH          Working directory for code execution
  --timeout SECONDS           Execution timeout
  --code-theme THEME          Syntax highlighting theme
  --verbose, -v               Enable verbose output
  --version                   Show version
  --help                      Show help message
```

## Contributing

Contributions are welcome! This project is in early development and there's lots to do.

### Roadmap

Current priorities:

- [ ] Native PDF output support
- [ ] Inline code evaluation (`<%= expression %>` syntax)
- [ ] Custom HTML templates (Jinja2)
- [ ] Watch mode for live development
- [ ] Rich display for more object types (NumPy arrays, scikit-learn models)
- [ ] Caching system for faster re-renders

See [issues](https://github.com/tresoldi/nhandu/issues) for more details and to suggest features.

## Project Information

### Citation

If you use Nhandu in your research, please cite:

```bibtex
@software{tresoldi2025nhandu,
  author = {Tresoldi, Tiago},
  title = {Nhandu: Literate Programming for Python},
  year = {2025},
  publisher = {Department of Linguistics and Philology, Uppsala University},
  address = {Uppsala, Sweden},
  url = {https://github.com/tresoldi/nhandu},
  orcid = {0000-0002-2863-1467}
}
```

### License

MIT License - see [LICENSE](LICENSE) file for details.

### Acknowledgments

Nhandu is inspired by:
- Donald Knuth's original [literate programming](https://en.wikipedia.org/wiki/Literate_programming) vision
- [knitr](https://yihui.org/knitr/) and R Markdown's approach to reproducible research
- [Jupyter](https://jupyter.org/)'s interactive computing paradigm
- [Quarto](https://quarto.org/)'s modern scientific publishing tools
- [Pweave](http://mpastell.com/pweave/)'s Python implementation (though no longer maintained)

Special thanks to the scientific Python community for building the ecosystem that makes tools like this possible.

---

**Status**: Early Development | **Python**: 3.10+ | **License**: MIT

[Documentation](https://github.com/tresoldi/nhandu) • [Examples](examples/) • [Issues](https://github.com/tresoldi/nhandu/issues) 
