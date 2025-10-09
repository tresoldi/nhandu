# Jupyter Notebook Integration

This tutorial demonstrates Nhandu's Jupyter notebook import and export capabilities, allowing you to bridge between notebook-based workflows and literate programming.

## Overview

Nhandu provides two-way conversion between:
- **Jupyter notebooks** (`.ipynb`) - Popular in data science and interactive computing
- **Nhandu literate Python** (`.py`) - Git-friendly, text-based literate programming

## Installation

The Jupyter integration requires an optional dependency:

```bash
pip install nhandu[jupyter]
```

This installs `nbformat`, the official Jupyter notebook format library (no kernel required).

## Importing from Jupyter

Convert a Jupyter notebook to Nhandu format:

```bash
nhandu import-notebook notebook.ipynb -o document.py
```

### What Happens During Import

1. **Markdown cells** → `#'` markdown comments
2. **Code cells** → Regular Python code
3. **Hidden cells** (with `hide` tag) → `#| hide` blocks
4. **Notebook metadata** → YAML frontmatter
5. **Outputs are discarded** (can be regenerated)

### Example

Given a Jupyter notebook `analysis.ipynb`:

**Markdown cell**:
```markdown
# Data Analysis

This notebook analyzes sample data.
```

**Code cell**:
```python
import numpy as np
data = np.random.randn(100)
print(f"Mean: {data.mean():.3f}")
```

Running:
```bash
nhandu import-notebook analysis.ipynb -o analysis.py
```

Produces `analysis.py`:
```python
#' # Data Analysis
#'
#' This notebook analyzes sample data.

import numpy as np
data = np.random.randn(100)
print(f"Mean: {data.mean():.3f}")
```

You can then process this with Nhandu:
```bash
nhandu analysis.py -o analysis.html
```

## Exporting to Jupyter

Convert a Nhandu literate Python file to Jupyter notebook:

```bash
nhandu export-notebook document.py -o notebook.ipynb
```

### What Happens During Export

1. **`#'` comments** → Markdown cells
2. **Regular code** → Code cells
3. **`#| hide` blocks** → Code cells with `hide` tag
4. **YAML frontmatter** → Notebook metadata
5. **No outputs by default** (symmetric with import)

### Example

Given a Nhandu file `report.py`:

```python
#' ---
#' title: My Report
#' author: Alice
#' ---
#'
#' # Introduction
#'
#' This is a report.

#| hide
import sys
CONFIG = {"debug": False}
#|

#' ## Analysis

import numpy as np
x = np.linspace(0, 10, 50)
print(f"Generated {len(x)} points")
```

Running:
```bash
nhandu export-notebook report.py -o report.ipynb
```

Creates a Jupyter notebook with:
- Metadata: `{"title": "My Report", "author": "Alice", ...}`
- Markdown cell: "# Introduction\n\nThis is a report."
- Code cell with `hide` tag: `import sys\nCONFIG = {"debug": False}`
- Markdown cell: "## Analysis"
- Code cell: `import numpy as np\nx = np.linspace(0, 10, 50)\nprint(f"Generated {len(x)} points")`

Open in Jupyter and run cells to generate outputs.

## Optional: Execute on Export

You can execute the notebook during export:

```bash
nhandu export-notebook document.py -o notebook.ipynb --execute
```

This runs all cells and includes outputs in the exported notebook.

You can specify a different kernel:
```bash
nhandu export-notebook document.py -o notebook.ipynb --execute --kernel python3
```

## Round-Trip Workflow

The import and export functions are designed to work together:

```bash
# Start with a Jupyter notebook
nhandu import-notebook original.ipynb -o literate.py

# Edit literate.py with your favorite editor
# (Benefits: git-friendly, plain text, no JSON)

# Convert back to Jupyter if needed
nhandu export-notebook literate.py -o modified.ipynb
```

### Round-Trip Preservation

Nhandu uses **best-effort** preservation:

✅ **Preserved**:
- Cell types (markdown, code)
- Cell content and structure
- Basic metadata (title, author)
- Hidden cell tags

⚠️ **Limitations**:
- Output cells are discarded on import (regeneratable)
- Some complex notebook metadata may be simplified
- Cell execution counts are not preserved
- Rich outputs (images, HTML) need regeneration

This is intentional - Nhandu focuses on the *source* (code + docs), not ephemeral outputs.

## Use Cases

### 1. Git-Friendly Notebooks

```bash
# Convert notebook to text format for version control
nhandu import-notebook analysis.ipynb -o analysis.py

# Commit the .py file (clean diffs!)
git add analysis.py
git commit -m "Add data analysis"

# Collaborators can convert back to notebook
nhandu export-notebook analysis.py -o analysis.ipynb
```

### 2. Notebook → Report Workflow

```bash
# Start with notebook
jupyter notebook experiment.ipynb

# Convert to Nhandu
nhandu import-notebook experiment.ipynb -o experiment.py

# Generate publication-ready HTML
nhandu experiment.py -o report.html
```

### 3. Code Review Without Jupyter

```bash
# Convert colleague's notebook to readable Python
nhandu import-notebook model.ipynb -o model.py

# Review in any text editor
# No Jupyter server needed!
```

### 4. Mixed Workflows

```bash
# Exploratory analysis in Jupyter
jupyter lab data_exploration.ipynb

# Export to Nhandu for final report
nhandu import-notebook data_exploration.ipynb -o report.py

# Edit and enhance with literate programming
vim report.py  # Add narrative, hide setup code, etc.

# Generate final outputs
nhandu report.py -o final_report.html
```

## Comparison: Jupyter vs Nhandu

| Feature | Jupyter Notebook | Nhandu Literate Python |
|---------|------------------|------------------------|
| **Format** | JSON (`.ipynb`) | Python (`.py`) |
| **Git diffs** | Messy (JSON + outputs) | Clean (plain text) |
| **Editor** | Browser required | Any text editor |
| **Execution** | Interactive (kernel) | Batch (script) |
| **Outputs** | Inline, preserved | Regenerated on demand |
| **Best for** | Exploration, teaching | Reports, documentation |

Both have strengths - use the conversion tools to get the best of both worlds!

## Tips and Best Practices

### 1. Clean Notebooks Before Import

Remove unnecessary outputs and execution counts in Jupyter:

```bash
# In Jupyter: Cell > All Output > Clear
```

This isn't required (outputs are discarded anyway), but keeps the import clean.

### 2. Use Metadata

Add metadata to notebooks for better conversion:

```python
# In first cell of notebook:
#' ---
#' title: My Analysis
#' author: Your Name
#' ---
```

This becomes YAML frontmatter in Nhandu format.

### 3. Mark Hidden Cells

In Jupyter, add the `hide` tag to cells you want hidden:

1. Select cell
2. View → Cell Toolbar → Tags
3. Add tag: `hide`

These become `#| hide` blocks in Nhandu.

### 4. Test Round-Trip Conversion

Before committing to a workflow, test the round-trip:

```bash
nhandu import-notebook original.ipynb -o test.py
nhandu export-notebook test.py -o roundtrip.ipynb
```

Compare `original.ipynb` and `roundtrip.ipynb` to verify structure preservation.

### 5. Use Verbose Mode

For debugging conversion issues:

```bash
nhandu import-notebook notebook.ipynb -o output.py --verbose
```

This shows what's being converted and any warnings.

## Limitations and Known Issues

### 1. Inline Code Expressions

Nhandu's inline code syntax (`<%= expression %>`) is converted to plain text when exporting to Jupyter, as Jupyter doesn't support this feature natively.

**Workaround**: Use f-strings in code cells instead:

```python
# Instead of:
#' The mean is <%= data.mean() %>

# Use:
mean = data.mean()
#' The mean is {mean}
```

### 2. Complex Metadata

Some advanced notebook metadata (widget state, execution timing, etc.) is not preserved.

### 3. Raw Cells

Jupyter's "raw" cells are converted to markdown code blocks in Nhandu format.

### 4. Multiple Outputs per Cell

Jupyter cells can have multiple outputs. Nhandu regenerates all outputs when running the document.

## Error Handling

### Import Errors

If import fails, check:

1. **Is nbformat installed?**
   ```bash
   pip install nbformat
   ```

2. **Is the notebook valid?**
   ```bash
   jupyter nbconvert --to notebook --execute notebook.ipynb
   ```

3. **Use verbose mode:**
   ```bash
   nhandu import-notebook notebook.ipynb -o output.py --verbose
   ```

### Export Errors

If export fails, check:

1. **Is the Python file valid?**
   ```bash
   python -m py_compile document.py
   ```

2. **Are there unmatched #| blocks?**
   Every `#| hide` needs a closing `#|`

3. **Use verbose mode:**
   ```bash
   nhandu export-notebook document.py -o output.ipynb --verbose
   ```

## Summary

Jupyter notebook integration in Nhandu provides:

- **Import**: Convert `.ipynb` → `.py` for git-friendly literate programming
- **Export**: Convert `.py` → `.ipynb` for Jupyter users
- **Round-trip**: Best-effort preservation of structure and metadata
- **Flexibility**: Use the right tool for each phase of your workflow

The key principle: **source over outputs**. Nhandu focuses on preserving the code and documentation, not ephemeral execution results. This makes version control cleaner and collaboration easier.

For more examples, see the other tutorials in the [`docs/`](https://github.com/tresoldi/nhandu/tree/main/docs/) directory.
