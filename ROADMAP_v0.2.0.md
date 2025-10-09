# Nhandu v0.2.0 - Feature Ideas and Improvements

**Status**: Planning / Brainstorming
**Target**: Next major release
**Current Version**: 0.1.3

---

## Guiding Principles for 0.2.0

1. **Simplicity First** - Features should be intuitive and add value without complexity
2. **Backward Compatible** - Existing documents should work without changes
3. **Production Quality** - Features should be well-tested and documented
4. **Git-Friendly** - Maintain text-first philosophy
5. **Performance** - Don't sacrifice speed for features

---

## Priority 1: Core Improvements (Already in Roadmap)

These are already identified as priorities and would make excellent 0.2.0 features:

### 1.1 Native PDF Output ⭐⭐⭐
**Value**: High - Many users need PDF for academic papers, reports
**Complexity**: Medium
**Dependencies**: ReportLab or WeasyPrint

**Implementation Options**:
```python
nhandu document.py --format pdf  # Direct PDF generation
nhandu document.py --format latex  # LaTeX intermediate (academic standard)
```

**Considerations**:
- Use WeasyPrint (HTML → PDF) for simplicity
- Or generate LaTeX → PDF for academic quality
- Need good math equation support
- Page breaks, headers/footers, TOC
- Custom page sizes and margins

**Estimated Effort**: 2-3 weeks

---

### 1.2 Custom HTML Templates (Jinja2) ⭐⭐⭐
**Value**: High - Users want branding, custom styles
**Complexity**: Medium
**Dependencies**: Jinja2 (already common in Python ecosystem)

**Features**:
```python
# In YAML frontmatter:
#' ---
#' template: academic.html
#' custom_css: my-styles.css
#' ---

# Or CLI:
nhandu doc.py --template custom.html
```

**Built-in Templates**:
- `default.html` - Current style
- `academic.html` - Clean, LaTeX-like
- `report.html` - Corporate/business style
- `presentation.html` - Slide-like layout
- `blog.html` - Blog post style
- `minimal.html` - Bare-bones

**Template Variables**:
```jinja
{{ title }}
{{ author }}
{{ date }}
{{ blocks }}  # List of rendered blocks
{{ toc }}     # Auto-generated table of contents
{{ metadata }}
```

**Estimated Effort**: 2 weeks

---

### 1.3 Watch Mode for Live Development ⭐⭐⭐
**Value**: High - Instant feedback during development
**Complexity**: Low-Medium
**Dependencies**: watchdog

**Usage**:
```bash
nhandu watch document.py          # Auto-rebuild on save
nhandu watch document.py --open   # Also open in browser
nhandu watch docs/*.py            # Watch multiple files
```

**Features**:
- File system watcher (detects changes)
- Automatic rebuild on save
- Browser auto-reload (optional HTTP server)
- Error notifications
- Smart debouncing (avoid rebuilding too frequently)

**Estimated Effort**: 1 week

---

### 1.4 Rich Display for More Object Types ⭐⭐
**Value**: Medium-High - Better visualization
**Complexity**: Medium
**Dependencies**: None (most are optional)

**Current Support**: pandas DataFrames, matplotlib figures, basic types

**Add Support For**:
- **NumPy arrays** (show shape, dtype, preview)
- **Scikit-learn models** (parameters, scores, visualization)
- **Pillow/PIL images** (display inline)
- **NetworkX graphs** (with matplotlib backend)
- **Seaborn plots** (already works, but optimize)
- **Plotly interactive plots** (embed as HTML)
- **SymPy expressions** (LaTeX rendering)
- **SQLAlchemy tables** (schema preview)
- **JSON/dict** (pretty-printed, collapsible)

**Implementation**:
```python
# In executor.py, add display hooks
def _display_object(obj):
    if isinstance(obj, np.ndarray):
        return _display_numpy(obj)
    elif isinstance(obj, sklearn.BaseEstimator):
        return _display_sklearn(obj)
    # etc.
```

**Estimated Effort**: 2-3 weeks (depends on how many types)

---

### 1.5 Caching System for Faster Re-renders ⭐⭐
**Value**: High - Speed up iteration
**Complexity**: Medium-High
**Dependencies**: None (use pickle or json)

**Features**:
- Cache executed code blocks by content hash
- Only re-execute changed blocks
- Cache figures and outputs
- Smart invalidation (detect variable dependencies)
- Option to clear cache

**Usage**:
```bash
nhandu doc.py --cache           # Enable caching
nhandu doc.py --no-cache        # Disable
nhandu doc.py --clear-cache     # Clear and rebuild
```

**Implementation**:
```python
# Hash code content + dependencies
cache_key = hash(code_content + str(dependencies))
if cache_key in cache:
    return cached_output
```

**Challenges**:
- Detecting dependencies between blocks
- Cache invalidation
- Handling side effects (file I/O, network)
- Cache storage location

**Estimated Effort**: 3-4 weeks

---

## Priority 2: User Experience Enhancements

### 2.1 Table of Contents Generation ⭐⭐⭐
**Value**: High - Essential for long documents
**Complexity**: Low

**Features**:
```python
#' ---
#' toc: true
#' toc_depth: 3  # Include h1-h3
#' ---
```

- Auto-generate from headings
- Clickable links (HTML)
- Page numbers (PDF)
- Sidebar TOC (floating)
- Collapsible sections

**Estimated Effort**: 3-4 days

---

### 2.2 Code Execution Control ⭐⭐
**Value**: Medium - More control over execution
**Complexity**: Low-Medium

**Features**:
```python
# Skip execution but show code
#| eval=false
expensive_computation()
#|

# Execute but don't show code
#| echo=false
setup_code()
#|

# Show code but don't execute (example)
#| eval=false, echo=true
dangerous_operation()
#|

# Execute multiple times with different params
#| params={"n": [10, 100, 1000]}
run_benchmark(n)
#|
```

**Block Options**:
- `eval` - Execute code (default: true)
- `echo` - Show code in output (default: true)
- `include` - Include in output (default: true)
- `cache` - Cache this block (default: false)
- `error` - Continue on error (default: true)
- `warning` - Show warnings (default: true)

**Estimated Effort**: 1 week

---

### 2.3 Cross-References and Links ⭐⭐
**Value**: Medium - Professional documents need this
**Complexity**: Low-Medium

**Features**:
```python
#' See @fig:scatter for details.
#' As shown in @tbl:results, the mean is 42.
#' Equation @eq:einstein proves this.

# Automatic numbering:
plt.figure()
plt.plot(x, y)
#' @fig:scatter This is my scatter plot

# Tables:
print(df)
#' @tbl:results Summary statistics

# Equations:
#' $$ E = mc^2 $$ @eq:einstein
```

**Estimated Effort**: 1-2 weeks

---

### 2.4 Export to Jupyter Notebook ⭐⭐
**Value**: Medium - Bridge between ecosystems
**Complexity**: Low

**Usage**:
```bash
nhandu export-notebook document.py -o document.ipynb
nhandu import-notebook notebook.ipynb -o document.py
```

**Features**:
- Convert `.py` → `.ipynb` (with outputs)
- Convert `.ipynb` → `.py` (preserve structure)
- Preserve metadata
- Handle cell types (markdown, code, raw)

**Estimated Effort**: 1 week

---

### 2.5 Bibliography and Citations ⭐⭐
**Value**: Medium-High - Academic papers need this
**Complexity**: Medium
**Dependencies**: pybtex or citeproc-py

**Features**:
```python
#' ---
#' bibliography: references.bib
#' citation_style: apa
#' ---
#'
#' According to @smith2020, the results are...
#' Multiple citations [@jones2019; @lee2021]
```

**Citation Styles**: APA, MLA, Chicago, IEEE, Nature, Science

**Estimated Effort**: 2 weeks

---

## Priority 3: Advanced Features

### 3.1 Notebook-Style Cell Execution ⭐⭐
**Value**: Medium - Jupyter users expect this
**Complexity**: High

**Features**:
- Execute individual cells (not whole document)
- Cell execution counter
- Variable inspector
- Incremental execution (only run cells after changes)

**Challenge**: Requires rethinking execution model

**Estimated Effort**: 3-4 weeks

---

### 3.2 Interactive HTML Widgets ⭐
**Value**: Low-Medium - Nice to have
**Complexity**: High
**Dependencies**: ipywidgets or custom

**Features**:
```python
from nhandu.widgets import slider, dropdown

#' Interactive parameter:
threshold = slider(0, 100, default=50, label="Threshold")
#' Current value: <%= threshold %>
```

**Challenge**: Requires JavaScript, client-side execution

**Estimated Effort**: 4+ weeks

---

### 3.3 Multi-Language Support ⭐
**Value**: Low-Medium - Useful for polyglot projects
**Complexity**: Very High
**Dependencies**: Kernel system (like Jupyter)

**Languages**: R, Julia, bash, SQL

**Example**:
```python
#' ```r
#' library(ggplot2)
#' ggplot(data, aes(x, y)) + geom_point()
#' ```
```

**Challenge**: Requires kernel management, IPC

**Estimated Effort**: 6+ weeks (major feature)

---

### 3.4 Collaborative Features ⭐
**Value**: Low - Nice to have
**Complexity**: Very High

**Features**:
- Comments/annotations
- Track changes
- Version comparison
- Diff tool for .py files
- Export to GitHub Gist

**Challenge**: Requires storage, UI

**Estimated Effort**: 8+ weeks

---

## Priority 4: Developer Experience

### 4.1 VS Code Extension ⭐⭐⭐
**Value**: High - Where developers work
**Complexity**: Medium
**Dependencies**: VS Code API

**Features**:
- Syntax highlighting for `#'` comments
- Preview pane (live render)
- Code folding for blocks
- Snippets for common patterns
- Run/preview commands
- Cell execution buttons

**Estimated Effort**: 3-4 weeks

---

### 4.2 Format Command ⭐⭐
**Value**: Medium - Consistency
**Complexity**: Low

**Usage**:
```bash
nhandu format document.py  # Format literate code
nhandu lint document.py    # Check for issues
```

**Features**:
- Normalize `#'` comment style
- Fix indentation
- Sort imports
- Check for common mistakes
- Validate frontmatter

**Estimated Effort**: 1 week

---

### 4.3 Test Mode ⭐⭐
**Value**: Medium - CI/CD integration
**Complexity**: Low

**Usage**:
```bash
nhandu test document.py       # Just verify it runs
nhandu test docs/*.py --fast  # Parallel testing
```

**Features**:
- Verify code executes without errors
- Don't generate output files
- Fast mode (skip plots, heavy computations)
- Exit codes for CI/CD
- Regression testing (compare outputs)

**Estimated Effort**: 3-4 days

---

### 4.4 Pre-commit Hooks ⭐
**Value**: Low-Medium - Quality assurance
**Complexity**: Low

**Setup**:
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/tresoldi/nhandu
  hooks:
    - id: nhandu-format
    - id: nhandu-lint
    - id: nhandu-test
```

**Estimated Effort**: 2-3 days

---

## Priority 5: Performance Improvements

### 5.1 Incremental Builds ⭐⭐
**Value**: Medium - Speed
**Complexity**: Medium

**Features**:
- Only rebuild changed files
- Dependency tracking
- Smart invalidation

**Estimated Effort**: 2 weeks

---

### 5.2 Parallel Processing ⭐
**Value**: Low-Medium - Speed for multiple files
**Complexity**: Low

**Usage**:
```bash
nhandu docs/*.py --parallel  # Process files in parallel
```

**Estimated Effort**: 3-4 days

---

### 5.3 Streaming Output ⭐
**Value**: Low - UX for long scripts
**Complexity**: Medium

**Features**:
- Show output as script runs
- Progress bar
- Partial results available

**Estimated Effort**: 1 week

---

## Recommended 0.2.0 Feature Set

Based on **value, effort, and alignment** with project goals:

### Must Have (Core)
1. ✅ **PDF Output** - Essential for academic users
2. ✅ **Custom HTML Templates** - High value, requested feature
3. ✅ **Watch Mode** - Developer productivity
4. ✅ **TOC Generation** - Essential for long documents

### Should Have (Enhancement)
5. ✅ **Rich Display Types** - NumPy, sklearn, Plotly
6. ✅ **Code Execution Control** - `eval`, `echo`, `include` options
7. ✅ **Table of Contents** - Auto-generated, collapsible
8. ✅ **Export to Jupyter** - Ecosystem bridge

### Nice to Have (If Time)
9. ⚠️ **Caching System** - If performance becomes issue
10. ⚠️ **VS Code Extension** - Major UX improvement
11. ⚠️ **Bibliography/Citations** - Academic users
12. ⚠️ **Test Mode** - CI/CD integration

---

## Implementation Strategy

### Phase 1: Core Features (Weeks 1-6)
- Week 1-2: **Watch Mode** (quick win)
- Week 3-4: **PDF Output** (LaTeX intermediate)
- Week 5-8: **Custom Templates** (includes built-ins)

### Phase 2: Enhancements (Weeks 7-10)
- Week 7-8: **TOC Generation**
- Week 9-10: **Rich Display Types** (NumPy, sklearn)
- Week 11: **Code Execution Control**

### Phase 3: Polish (Weeks 11-12)
- Week 12: **Export to Jupyter**
- Week 13: **Test Mode**
- Week 14: Documentation, examples, testing

---

## Breaking Changes to Avoid

- Keep all existing CLI flags
- Maintain current file format
- Don't change default behavior
- Provide migration guide if needed

---

## Testing Requirements

For each feature:
- Unit tests (pytest)
- Integration tests (full workflow)
- Example documents
- Documentation
- CI/CD validation

---

## Documentation Requirements

For each feature:
- README.md section
- Tutorial in docs/
- API reference
- Migration guide (if breaking)
- Example code

---

## Community Input

Consider:
- GitHub Discussions for feature voting
- Survey existing users
- Look at similar tools (Quarto, R Markdown)
- Academic user feedback

---

## Success Metrics for 0.2.0

- [ ] PDF output comparable to LaTeX quality
- [ ] Watch mode with <1s rebuild time
- [ ] 5+ high-quality templates
- [ ] Support for 8+ rich object types
- [ ] 95%+ backward compatibility
- [ ] CI passing on all features
- [ ] Documentation complete
- [ ] 3+ academic papers published using Nhandu

---

## Beyond 0.2.0 (0.3.0 Ideas)

- Interactive widgets
- Multi-language support (R, Julia)
- Cloud rendering service
- Mobile-friendly output
- Presentation mode
- Dark mode support
- Collaborative editing
- Plugin system

---

## Notes

- **Scope Control**: 0.2.0 should be achievable in 3-4 months
- **Quality Over Quantity**: 4 excellent features > 10 mediocre ones
- **User Focus**: Prioritize academic/scientific users (core audience)
- **Simplicity**: Each feature should "just work" with smart defaults

---

## Feedback Welcome

This is a living document. Please contribute ideas via:
- GitHub Issues
- GitHub Discussions
- Email: tiago.tresoldi@lingfil.uu.se
