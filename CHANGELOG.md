# Changelog

All notable changes to Nhandu will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-10-27

### BREAKING CHANGES

**Nhandu is now Python-only literate programming.** Traditional markdown (`.md`) file support has been removed to simplify the codebase and provide a clearer, more focused vision.

### Removed
- **Markdown file format support (`.md` files)** - Complete removal of dual-format support
  - Deleted `src/nhandu/parser.py` (markdown parser)
  - Removed all `.md` test fixtures (6 files) and example docs (5 files)
  - Removed markdown format detection from CLI
- All references to `.md` format in README and documentation

### Changed
- **Unified parser**: `parser_py.py` renamed to `parser.py` and is now the only parser
  - `parse()` function now always parses Python literate format (`#'` comments)
  - `parse_python()` provided as backward compatibility alias
- **CLI simplified**: Removed format auto-detection, always expects `.py` files
  - Updated help text: "Input file to process (.py literate Python)"
- **README**: Removed "Traditional Markdown Format" section and all `.md` mentions
- **Project focus**: Clear Python-first philosophy - one format, one parser, one way

### Why This Change?

Nhandu's value proposition is **literate programming in plain Python files**. Supporting both formats:
- Split focus and complicated the codebase
- Confused users about which format to use
- Maintained two parsers for essentially the same functionality
- Diluted the "Python-native" messaging

Going forward, Nhandu is about one thing: writing beautiful, executable documents in `.py` files using `#'` comments for markdown. This makes the tool simpler, more maintainable, and more aligned with its core vision.

### Migration Notes

If you have existing `.md` files, manual conversion is straightforward:

**From markdown**:
````markdown
# My Document

Text here.

```python
code_here()
```
````

**To Python literate**:
```python
#' # My Document
#'
#' Text here.

code_here()
```

The pattern: move markdown outside code blocks to `#'` comments, code blocks become regular Python.

### Technical Details
- Simplified import structure in `__init__.py` and `__main__.py`
- Updated all test imports from `parse_python` to `parse`
- Rewrote `test_parser.py` to test Python literate format exclusively
- Parser module structure unified (one file, clear responsibility)
- Version bumped to 0.3.0 to indicate breaking change

## [0.2.0] - 2025-10-09

### Added
- **Jupyter Notebook Integration** - Full import/export support for Jupyter notebooks
  - New CLI command: `nhandu import-notebook` - Convert `.ipynb` → `.py` literate format
  - New CLI command: `nhandu export-notebook` - Convert `.py` → `.ipynb` notebook format
  - Conversion features:
    - Markdown cells ↔ `#'` markdown comments
    - Code cells ↔ Regular Python code
    - Hidden cells (with `hide` tag) ↔ `#| hide` blocks
    - Notebook metadata ↔ YAML frontmatter
    - Outputs discarded on import (regeneratable)
    - No outputs on export by default (symmetric with import)
  - Optional `--execute` flag to run notebook cells during export
  - Optional `--kernel` parameter for kernel selection
  - Round-trip conversion support with best-effort preservation
  - Comprehensive test suite with 14 tests covering import, export, and round-trip
  - Tutorial documentation (`docs/07_jupyter_conversion.md`)
- New optional dependency group `[jupyter]` with `nbformat>=5.0`
- Graceful error handling when nbformat not installed (with install instructions)
- Inline code conversion: `<%= expr %>` converted to f-strings where possible during export
- 4 test fixture notebooks for testing various conversion scenarios
- **Python Script Environment Variables** - Full support for standard Python special variables
  - `__file__`: Set to absolute path of source document (enables `Path(__file__).parent` pattern)
  - `__name__`: Always set to `"__main__"` (matches script execution behavior)
  - `__builtins__`: Full access to built-in functions (len, print, type, etc.)
  - `sys.argv[0]`: Set to match `__file__` for script-like behavior
  - `sys.path[0]`: Includes script directory for relative imports
  - Fallback for stdin/in-memory: `__file__` set to `<stdin>` in current directory
  - Context manager ensures sys.path and sys.argv are restored after execution
  - Test suite with 14 tests covering all special variables and real-world usage
  - Enables loading data files relative to script location
  - Supports importing modules from script directory

### Changed
- Project structure: Added `src/nhandu/converters/` module for format conversion
- README.md: Added "Jupyter Notebook Integration" section with usage examples
- CLI: Enhanced argument parser to support subcommands while maintaining backward compatibility
- CLI help now includes separate documentation for notebook commands

### Documentation
- Comprehensive Jupyter integration tutorial with examples and best practices
- Updated README with import/export workflow examples
- Added comparison table: Jupyter vs Nhandu literate Python
- Documented use cases: git-friendly notebooks, report generation, code review
- Added tips for metadata preservation and round-trip conversion
- Updated roadmap to reference detailed v0.2.0 planning document

### Technical Details
- New module: `nhandu.converters.notebook` with import/export functions
- Cell type mapping: markdown, code, raw cells handled appropriately
- Metadata extraction from notebook to YAML frontmatter
- Python comment preservation during round-trip conversion
- Best-effort structural preservation (cell order, types, content)
- Enhanced `CodeExecutor._create_initial_namespace()` to include special variables
- New `_script_environment()` context manager for sys.path and sys.argv management
- Automatic restoration of global state (sys.path, sys.argv) after execution
- Absolute paths used for `__file__` to match Python's standard behavior

## [0.1.3] - 2025-10-09

### Added
- Comprehensive inline code evaluation documentation
  - Added "Inline Code Evaluation" section to README.md with syntax and examples
  - Updated LLM_DOCS.md with inline code syntax, examples, and best practices
  - Added inline code entries to Quick Reference Card
  - Created `examples/06_inline_code.py` - comprehensive example demonstrating all inline code features
- 13 new tests for inline code in Python literate format (`test_inline_python_literate.py`)
- 5 new tests for HTML title generation (`test_renderer.py`)

### Fixed
- HTML title generation now uses intelligent fallback logic
  - Priority: 1) YAML frontmatter `title`, 2) source filename (without extension), 3) default "Nhandu Report"
  - Previously all files without frontmatter title showed generic "Nhandu Report"
  - Added `_get_document_title()` method to HTMLRenderer
- Corrected misleading documentation that listed inline code as "not implemented"
  - Feature was fully functional but undocumented
  - Removed from roadmap, added to features documentation

### Changed
- All example files (01-06) now include YAML frontmatter with proper titles
- Updated README.md examples list to include new inline code example

### Documentation
- Inline code syntax: `<%= expression %>` for display, `<% statement %>` for execution
- Examples show integration with regular code blocks, hidden blocks, and formatting
- Clear guidance on when to use inline code vs regular code blocks

## [0.1.2] - 2025-10-06

### Added
- GitHub Flavored Markdown (GFM) support in HTML output
  - Tables now render correctly as HTML `<table>` elements
  - Strikethrough syntax (`~~text~~`) support
  - Footnotes syntax (`[^1]`) support
- 11 comprehensive tests for markdown features (tables, strikethrough, footnotes)

### Fixed
- Markdown tables were rendering as plain paragraphs with literal pipe characters
- Missing mistune plugins prevented GFM features from working

### Changed
- Updated HTML renderer to use `mistune.create_markdown()` with plugins instead of basic `mistune.Markdown()`

## [0.1.1] - 2025-10-06

### Added
- Empty block filtering in parsers
  - Filters code blocks with only whitespace or comments
  - Filters markdown blocks with only whitespace/newlines
  - Filters empty hidden blocks
  - Defensive rendering (preserves blocks with execution output/errors)
- "Made with Nhandu" footer in HTML output
  - Centered at bottom with professional styling
  - Links to PyPI project page
  - Configurable via `show_footer` metadata field (default: true)
  - Can be disabled with `--no-footer` CLI flag
  - HTML only (not in markdown output)
- 15 tests for empty block filtering
- 13 tests for footer functionality

### Changed
- HTML renderer now includes footer CSS styling
- Document metadata now includes `show_footer` field

## [0.1.0] - 2025-09-30

### Added
- Initial release of Nhandu
- Core literate programming functionality
  - Python literate format (`.py` files with `#'` markdown comments)
  - Traditional markdown format (`.md` files with code blocks)
  - Sequential code execution with shared namespace
- Output formats
  - HTML with syntax highlighting (via Pygments)
  - Markdown output
- Smart output capture
  - Print statements and stdout
  - Matplotlib plots (automatic capture, no `plt.show()` needed)
  - Expression results (Jupyter-like behavior)
  - Rich objects (pandas DataFrames as HTML tables)
- Hidden code blocks (`#| hide` ... `#|`)
- YAML frontmatter support for configuration
- CLI with multiple options
  - Input/output file specification
  - Format selection (`--format`)
  - Working directory (`--working-dir`)
  - Execution timeout (`--timeout`)
  - Syntax highlighting themes (`--code-theme`)
  - Verbose mode (`--verbose`)
- Configuration via YAML files
- Server-side syntax highlighting with 50+ Pygments themes
- Default theme: `github-dark`
- Comprehensive test suite with pytest
- Type checking with mypy
- Linting with ruff
- Example files demonstrating various features

### Technical Details
- Python 3.10+ required
- Dependencies: PyYAML, mistune, Pygments
- Optional: matplotlib, numpy, pandas (for examples/tests)
- MIT License

[0.2.0]: https://github.com/tresoldi/nhandu/compare/v0.1.3...v0.2.0
[0.1.3]: https://github.com/tresoldi/nhandu/compare/v0.1.2...v0.1.3
[0.1.2]: https://github.com/tresoldi/nhandu/compare/v0.1.1...v0.1.2
[0.1.1]: https://github.com/tresoldi/nhandu/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/tresoldi/nhandu/releases/tag/v0.1.0
