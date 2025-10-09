# Changelog

All notable changes to Nhandu will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
