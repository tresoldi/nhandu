# Nhandu vs. PROJECT_STRUCTURE_TEMPLATE.md Comparison Report

**Date**: 2025-10-09
**Template Version**: PROJECT_STRUCTURE_TEMPLATE.md
**Project**: Nhandu 0.1.3

---

## Executive Summary

Nhandu follows many of the template's principles but has several significant differences, primarily in:
- **Version management** (hardcoded vs. dynamic)
- **Package structure** (src-layout vs. flat root)
- **Missing components** (no docs/, scripts/, .github/, py.typed)
- **Coverage enforcement** (no threshold set)
- **Documentation approach** (examples/ vs. docs/tutorials)
- **Makefile capabilities** (basic vs. comprehensive)

---

## 1. Directory Structure Comparison

### ✅ What Matches

```
nhandu/
├── examples/          # Similar to docs/ but different purpose
│   └── figures/       # ✓ Figures directory present
├── tests/             # ✓ Test directory
│   ├── test_*.py      # ✓ Test modules
│   ├── fixtures/      # Additional: fixture files
│   └── htmlcov/       # ✓ Coverage reports (gitignored)
├── src/nhandu/        # ✓ Source layout (template uses flat)
│   ├── __init__.py    # ✓ With __version__
│   └── *.py           # ✓ Core modules
├── .gitignore         # ✓ Present
├── CHANGELOG.md       # ✓ Keep a Changelog format
├── LICENSE            # ✓ MIT License
├── Makefile           # ✓ Present (but simplified)
├── pyproject.toml     # ✓ Centralized config
└── README.md          # ✓ Project overview
```

### ❌ What's Different

| Template | Nhandu | Impact |
|----------|--------|--------|
| `project_name/` (flat) | `src/nhandu/` (src-layout) | Minor - src-layout is also valid |
| `docs/tutorial_*.py` | `examples/*.py` | Different naming/purpose |
| Version in `__init__.py` only | Version in both `__init__.py` AND `pyproject.toml` | **CRITICAL** - violates single source of truth |
| `docs/` directory | No `docs/` | Missing structured documentation |
| `scripts/` directory | No `scripts/` | Missing benchmarks/utilities |
| `.github/workflows/` | No `.github/` | **CRITICAL** - No CI/CD |
| `py.typed` marker | Missing | Type checking not advertised |

### ❌ Missing Components

1. **No `.github/` directory**
   - No CI/CD workflows
   - No automated quality checks
   - No dependabot.yml

2. **No `docs/` directory**
   - No API_REFERENCE.md
   - No USER_GUIDE.md
   - No structured tutorial system

3. **No `scripts/` directory**
   - No benchmarks.py
   - No utility scripts

4. **No `py.typed` file**
   - Package doesn't declare PEP 561 compliance
   - Type stubs not advertised to mypy users

### ✅ What Nhandu Has (Not in Template)

- `figures/` in project root (in addition to examples/figures)
- `LLM_DOCS.md` in root (template has this in docs/)
- `tests/fixtures/` for test data
- `PUBLISH.md` (custom addition from this session)

---

## 2. Version Management - **CRITICAL DIFFERENCE**

### Template Approach (Recommended)

**Single source of truth in `__init__.py`**:

```toml
# pyproject.toml
[project]
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "project_name.__version__"}
```

```python
# __init__.py
__version__ = "0.1.0"
```

**Benefits**: One place to update, no sync issues

### Nhandu Approach (Current)

**Duplicated version in two places**:

```toml
# pyproject.toml
[project]
version = "0.1.3"  # ← Hardcoded
```

```python
# __init__.py
__version__ = "0.1.3"  # ← Also hardcoded
```

**Problems**:
- ❌ Violates DRY principle
- ❌ Risk of version mismatch
- ❌ Must update two files manually
- ❌ Error-prone during releases

**Recommendation**: Switch to dynamic version from `__init__.py`

---

## 3. Makefile - Capabilities Comparison

### Template Features (Comprehensive)

```makefile
✅ help                   # Self-documenting
✅ quality               # ruff format check + ruff check + mypy
✅ format                # Auto-format
✅ test                  # Basic tests
✅ test-cov              # With coverage threshold (80%)
✅ test-fast             # Parallel execution
✅ bump-version          # Automated version bump + tag
✅ build                 # Package build
✅ build-release         # Full release pipeline
✅ clean                 # Comprehensive cleanup
✅ install / install-dev # Dependency installation
✅ docs                  # Generate docs from tutorials
✅ docs-clean            # Clean generated docs
✅ bench                 # Run benchmarks
```

### Nhandu Features (Basic)

```makefile
✅ help                  # Basic list
✅ lint                  # mypy + ruff check + ruff format check
✅ format                # Auto-format
✅ test                  # Basic tests (no coverage threshold)
❌ test-cov              # Missing (uses pytest config instead)
❌ test-fast             # Missing
❌ bump-version          # Missing
❌ build                 # Missing
❌ build-release         # Missing
✅ clean                 # Present
✅ install / install-dev # Present
✅ examples              # Similar to docs (processes examples)
✅ clean-examples        # Similar to docs-clean
❌ bench                 # Missing
✅ all                   # lint + test
```

### Key Differences

1. **No version management target** - Template has automated bump-version
2. **No build targets** - Must use `python -m build` manually
3. **No test-cov target** - Coverage not enforced in Makefile
4. **No test-fast** - No parallel test execution
5. **No benchmarking** - No performance tracking
6. **Examples vs docs** - Different naming convention

**Quality command differs**:
- Template: `ruff format --check` + `ruff check` + `mypy` (three separate tools)
- Nhandu: Combined in `lint` target

---

## 4. pyproject.toml Configuration

### ✅ What Matches

- Build system: setuptools + wheel
- Project metadata structure
- License: MIT
- Dependencies structure
- Optional dependencies with `dev`, `test`, `all` groups
- Ruff configuration (mostly aligned)
- MyPy configuration (mostly aligned)
- Pytest configuration
- Coverage configuration

### ❌ Key Differences

#### 4.1 Version Management (CRITICAL)

**Template**:
```toml
dynamic = ["version"]

[tool.setuptools.dynamic]
version = {attr = "project_name.__version__"}
```

**Nhandu**:
```toml
version = "0.1.3"  # Hardcoded
# No dynamic version config
```

#### 4.2 Package Finding

**Template**:
```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["project_name*"]
```

**Nhandu**:
```toml
[tool.setuptools.packages.find]
where = ["src"]  # src-layout
# No include specified
```

Both valid, different conventions.

#### 4.3 Coverage Threshold

**Template**:
```toml
[tool.pytest.ini_options]
addopts = [
    "--cov-fail-under=80",  # ← ENFORCED
    # ...
]
```

**Nhandu**:
```toml
[tool.pytest.ini_options]
addopts = "--cov=nhandu --cov-report=term-missing --cov-report=html"
# NO --cov-fail-under specified! ← MISSING ENFORCEMENT
```

**Impact**: Tests pass even with low coverage

#### 4.4 Ruff Rules

**Template** has more comprehensive rules:
```toml
select = [
    "E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM",
    "ICN", "PIE", "T20", "PYI", "PT", "Q", "RSE", "RET",
    "TID", "TCH", "RUF", "D"  # ← Includes docstring checks
]
```

**Nhandu**:
```toml
select = [
    "E", "F", "W", "B", "I", "N", "UP", "ANN", "S",
    "C90", "T20", "RUF"
]
```

**Missing from Nhandu**:
- `D` (pydocstyle/docstrings)
- `ARG` (unused arguments)
- `SIM` (simplify)
- `PT` (pytest-style)
- Several others

**Nhandu has that template doesn't**:
- `ANN` (annotations) - stricter type hints
- `S` (bandit security)
- `N` (pep8-naming)
- `C90` (mccabe complexity)

#### 4.5 MyPy Strictness

**Template**:
```toml
[tool.mypy]
disallow_untyped_defs = true
disallow_incomplete_defs = true
warn_unreachable = true
# More strict settings
```

**Nhandu**:
```toml
[tool.mypy]
disallow_untyped_defs = true
# Less strict - missing some template settings
```

#### 4.6 Pytest Markers

**Template**: Defines markers (slow, integration, memory)
**Nhandu**: No markers defined

---

## 5. Documentation Structure

### Template Approach

```
docs/
├── tutorial_1_basics.py      # Executable tutorials
├── tutorial_2_advanced.py
├── tutorial_*.html           # Generated (gitignored)
├── figures/                  # Tutorial figures
├── API_REFERENCE.md          # API docs
├── USER_GUIDE.md             # User guide
└── LLM_DOCUMENTATION.md      # LLM-friendly
```

**Generation**: `make docs` → converts `.py` to `.html`

### Nhandu Approach

```
examples/
├── 01_hello_world.py         # Example files
├── 02_data_analysis.py
├── 03_plotting.py
├── ...
├── figures/                  # Example figures

# Root level:
LLM_DOCS.md                   # LLM-friendly (in root)
README.md                     # Main docs
```

**Generation**: `make examples` → creates `.out` and `.html` files

### Key Differences

1. **Naming**: `examples/` vs. `docs/`
2. **Purpose**: Examples are demonstrations, tutorials are learning paths
3. **Numbering**: Nhandu uses `01_`, `02_` prefixes
4. **Missing**: No API_REFERENCE.md, no USER_GUIDE.md
5. **LLM docs location**: Root vs. docs/ directory

---

## 6. Testing Organization

### Template

```
tests/
├── test_basic.py
├── test_advanced.py
├── test_numerical_stability.py
├── test_statistical_correctness.py
├── test_memory_management.py
├── test_property_based.py
├── test_regression_reference.py
```

**Features**:
- Property-based testing with hypothesis
- Specialized test categories
- 80% coverage threshold enforced
- Pytest markers for organization

### Nhandu

```
tests/
├── test_cli.py
├── test_empty_blocks.py
├── test_executor.py
├── test_footer.py
├── test_inline_python_literate.py
├── test_markdown_features.py
├── test_parser.py
├── test_renderer.py
├── fixtures/
```

**Current state**:
- ✅ Good organization by component
- ✅ 92% coverage achieved
- ❌ No coverage threshold enforcement
- ❌ No property-based testing
- ❌ No test markers defined
- ✅ Has fixtures/ directory (not in template)

---

## 7. GitHub Integration

### Template

```
.github/
├── workflows/
│   └── quality.yml           # CI/CD pipeline
└── dependabot.yml            # Automated updates
```

**Features**:
- Automated quality checks on push/PR
- Format checking with ruff
- Linting with ruff
- Type checking with mypy
- Tests with coverage threshold
- Runs on multiple Python versions

### Nhandu

**Status**: ❌ **MISSING ENTIRELY**

**Impact**:
- No automated quality checks
- No CI/CD validation
- No automated dependency updates
- Manual testing only
- Higher risk of regressions

---

## 8. Type Checking Support

### Template

```
project_name/
├── __init__.py
├── module.py
└── py.typed              # ← PEP 561 marker
```

**Purpose**: Declares package provides type hints

### Nhandu

```
src/nhandu/
├── __init__.py
├── *.py
# NO py.typed file
```

**Impact**:
- Type hints exist in code
- But package doesn't advertise PEP 561 compliance
- External type checkers may not recognize types

---

## 9. Development Workflow Comparison

### Template Workflow

```bash
# Initial setup
make install-dev

# Daily development
make format      # Auto-format
make quality     # Full quality check
make test-cov    # Tests with enforced coverage
make docs        # Generate documentation

# Release
make bump-version TYPE=minor  # Automated
make build-release            # Full pipeline
twine upload dist/*
```

### Nhandu Workflow (Current)

```bash
# Initial setup
make install-dev

# Daily development
make format      # Auto-format
make lint        # Quality check
make test        # Tests (no threshold)
make examples    # Generate example outputs

# Release (manual)
# 1. Edit __init__.py version
# 2. Edit pyproject.toml version
# 3. Edit CHANGELOG.md
# 4. Commit and tag manually
# 5. python -m build
# 6. twine upload dist/*
```

**Differences**:
- Nhandu requires manual version updates in 2 places
- No automated version bumping
- No integrated build pipeline
- More manual steps, more error-prone

---

## 10. Key Principles Adherence

### 10.1 Single Source of Truth

**Template**: ✅ Version in `__init__.py` only
**Nhandu**: ❌ Version in both files (violates principle)

### 10.2 Flat Package Structure

**Template**: Flat `project_name/` at root
**Nhandu**: src-layout `src/nhandu/` (also valid, different convention)

### 10.3 Coverage Enforcement

**Template**: ✅ 80% threshold enforced
**Nhandu**: ❌ No threshold (achieves 92% but not enforced)

### 10.4 CI/CD

**Template**: ✅ GitHub Actions
**Nhandu**: ❌ No CI/CD

### 10.5 Documentation

**Template**: ✅ Structured docs/ with tutorials + API + guides
**Nhandu**: ⚠️  Examples exist, formal docs missing

### 10.6 Type Safety

**Template**: ✅ py.typed marker
**Nhandu**: ❌ Missing py.typed

### 10.7 Automated Workflows

**Template**: ✅ Comprehensive Makefile with release automation
**Nhandu**: ⚠️  Basic Makefile, manual release process

---

## 11. Summary Table

| Feature | Template | Nhandu | Status |
|---------|----------|--------|--------|
| **Version Management** | Dynamic from `__init__.py` | Hardcoded in 2 places | ❌ Critical |
| **Package Layout** | Flat root | src-layout | ✅ Both valid |
| **Coverage Threshold** | 80% enforced | None (92% achieved) | ⚠️  Should enforce |
| **CI/CD** | GitHub Actions | None | ❌ Critical |
| **py.typed** | Yes | No | ❌ Minor |
| **docs/ directory** | Yes (tutorials) | No (examples instead) | ⚠️  Different approach |
| **scripts/** | Yes (benchmarks) | No | ❌ Minor |
| **Makefile** | Comprehensive | Basic | ⚠️  Functional |
| **Pytest markers** | Defined | None | ❌ Minor |
| **Property tests** | With hypothesis | None | ❌ Minor |
| **Auto version bump** | Yes | No | ❌ Medium |
| **Build targets** | Yes | No | ❌ Medium |
| **Ruff rules** | Extensive | Good | ✅ Adequate |
| **MyPy config** | Strict | Strict | ✅ Good |
| **Test organization** | By category | By component | ✅ Good |

---

## 12. Recommendations (Priority Order)

### 🔴 Critical (Should Fix)

1. **Version Management**: Switch to dynamic versioning from `__init__.py`
   - Remove hardcoded version from pyproject.toml
   - Add `[tool.setuptools.dynamic]` configuration

2. **CI/CD**: Add GitHub Actions workflow
   - Automated quality checks
   - Test coverage enforcement
   - Multi-version Python testing

3. **Coverage Enforcement**: Add `--cov-fail-under=80` to pytest config
   - Prevent coverage regressions
   - Currently at 92%, enforce minimum

### 🟡 Medium Priority (Should Consider)

4. **Makefile Enhancement**:
   - Add `bump-version` target
   - Add `build` and `build-release` targets
   - Add `test-cov` target explicitly

5. **Type Marker**: Add `src/nhandu/py.typed` file
   - One-line fix for PEP 561 compliance

6. **Documentation Structure**: Consider adding `docs/`
   - API_REFERENCE.md
   - USER_GUIDE.md
   - Move examples to docs/tutorials

### 🟢 Low Priority (Nice to Have)

7. **Test Organization**:
   - Add pytest markers (slow, integration)
   - Consider property-based tests with hypothesis

8. **Scripts Directory**:
   - Add benchmarks.py for performance tracking

9. **Ruff Rules**: Consider adding pydocstyle (`D`) rules
   - Improve docstring consistency

---

## 13. What Nhandu Does Well (Not in Template)

1. **LLM_DOCS.md** - Excellent LLM-friendly documentation
2. **Test fixtures** - Well-organized test data in fixtures/
3. **Security checks** - Ruff `S` rules (bandit)
4. **Type annotations** - Ruff `ANN` rules (stricter than template)
5. **High coverage** - 92% achieved (exceeds template's 80% goal)
6. **PUBLISH.md** - Clear release documentation

---

## Conclusion

Nhandu is a **well-structured project** that follows many modern Python best practices. The main gaps compared to the template are:

1. **Version management duplication** (critical fix needed)
2. **No CI/CD** (critical for production quality)
3. **Missing automated release workflow** (error-prone manual process)
4. **No coverage enforcement** (achieved but not enforced)

The project is already at 92% coverage and has good code quality. Adding the missing automation (CI/CD, version bumping, coverage enforcement) would align it fully with production-ready standards.

**Overall Assessment**: 75% template compliance, with critical automation gaps but excellent code quality.
