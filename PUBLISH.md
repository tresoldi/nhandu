# Publishing Nhandu v0.1.3 to PyPI

## Pre-Publication Checklist

✅ Version bumped to 0.1.3 in:
- pyproject.toml
- src/nhandu/__init__.py

✅ CHANGELOG.md updated with all changes

✅ All 108 tests passing (92% coverage)

✅ Distribution packages built successfully:
- dist/nhandu-0.1.3-py3-none-any.whl (20K)
- dist/nhandu-0.1.3.tar.gz (33K)

✅ Packages validated with twine check: PASSED

## Changes in v0.1.3

### Fixed
1. **Inline Code Documentation** - Feature was working but not documented
   - Removed misleading "not implemented" from roadmap
   - Added comprehensive documentation to README.md and LLM_DOCS.md
   - Created examples/06_inline_code.py
   - Added 13 new tests

2. **HTML Title Generation** - Now uses intelligent fallback
   - Priority: YAML title → filename → "Nhandu Report"
   - All examples updated with proper titles
   - Added 5 new tests

### Summary
- 18 new tests added (13 inline code + 5 title)
- Total tests: 108 (all passing)
- No breaking changes
- Documentation improvements

## Publishing Steps

### 1. Create and Push Git Tag

```bash
# Create annotated tag
git add -A
git commit -m "Bump version to 0.1.3"
git tag -a v0.1.3 -m "Release v0.1.3: Inline code docs + HTML title fix"

# Push commits and tag
git push origin main
git push origin v0.1.3
```

### 2. Publish to PyPI

You have two options:

#### Option A: Publish to Production PyPI (Recommended)

```bash
# Upload to PyPI (production)
python -m twine upload dist/*

# You will be prompted for:
# - Username: __token__
# - Password: <your PyPI API token>
```

#### Option B: Test on TestPyPI First (Safer)

```bash
# Upload to TestPyPI first
python -m twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ nhandu==0.1.3

# If everything works, then upload to production PyPI
python -m twine upload dist/*
```

### 3. Verify Publication

After publishing, verify the release:

```bash
# Wait a minute for PyPI to update, then:
pip install --upgrade nhandu

# Check version
python -c "import nhandu; print(nhandu.__version__)"
# Should output: 0.1.3

# Test CLI
nhandu --version
# Should output: nhandu 0.1.3
```

### 4. Create GitHub Release

1. Go to https://github.com/tresoldi/nhandu/releases/new
2. Select tag: v0.1.3
3. Release title: "v0.1.3 - Inline Code Documentation & HTML Title Fix"
4. Description: Copy from CHANGELOG.md section for 0.1.3
5. Attach dist files (optional):
   - dist/nhandu-0.1.3-py3-none-any.whl
   - dist/nhandu-0.1.3.tar.gz
6. Publish release

## PyPI API Token Setup (if needed)

If you don't have a PyPI API token configured:

1. Go to https://pypi.org/manage/account/token/
2. Create new token with scope "Entire account" or "Project: nhandu"
3. Copy the token (starts with `pypi-`)
4. Configure in ~/.pypirc:

```ini
[pypi]
username = __token__
password = pypi-YOUR_TOKEN_HERE
```

Or use it directly when prompted by twine.

## Post-Publication

After successful publication:

1. ✅ Verify package on PyPI: https://pypi.org/project/nhandu/
2. ✅ Test installation: `pip install --upgrade nhandu`
3. ✅ Create GitHub release
4. ✅ Announce on relevant channels (if applicable)

## Rollback (if needed)

PyPI doesn't allow deleting releases, but you can:

```bash
# Upload a hotfix version
# Edit pyproject.toml and __init__.py to 0.1.4
python -m build
python -m twine upload dist/nhandu-0.1.4*
```

## Files Modified in This Release

- CHANGELOG.md - Added v0.1.3 entry
- pyproject.toml - Version 0.1.2 → 0.1.3
- src/nhandu/__init__.py - Version 0.1.2 → 0.1.3
- src/nhandu/renderer.py - Added _get_document_title()
- README.md - Added inline code docs, updated examples
- LLM_DOCS.md - Added inline code syntax
- examples/01-06 - Added title frontmatter
- examples/06_inline_code.py - NEW
- tests/test_inline_python_literate.py - NEW
- tests/test_renderer.py - Added 5 title tests

---

Ready to publish! Run the git and twine commands above when ready.
