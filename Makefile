.PHONY: help install install-dev test test-cov lint quality format bump-version build build-release docs docs-clean clean all

TYPE ?= patch  # For version bumping: patch, minor, or major

help:
	@echo "Available commands:"
	@echo "  make install        Install nhandu in production mode"
	@echo "  make install-dev    Install nhandu with dev and test dependencies"
	@echo "  make test           Run tests with coverage"
	@echo "  make test-cov       Run tests with coverage report (enforces 80% threshold)"
	@echo "  make lint           Run mypy and ruff checks"
	@echo "  make quality        Alias for lint"
	@echo "  make format         Format code with ruff"
	@echo "  make bump-version   Bump version (TYPE=patch|minor|major), commit and tag"
	@echo "  make build          Build distribution packages"
	@echo "  make build-release  Full release build (clean → lint → test → build)"
	@echo "  make docs           Generate documentation from all tutorial files"
	@echo "  make docs-clean     Remove generated documentation"
	@echo "  make clean          Remove build artifacts and cache"
	@echo "  make all            Run lint and test"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev,test]"

test:
	pytest

lint:
	mypy src/nhandu
	ruff check src/nhandu tests
	ruff format --check src/nhandu tests

format:
	ruff format src/nhandu tests
	ruff check --fix src/nhandu tests

test-cov:
	pytest --cov=nhandu --cov-report=html:tests/htmlcov --cov-report=term-missing --cov-fail-under=80 tests/

quality: lint

bump-version:
	@CURRENT=$$(grep -o "__version__ = \"[^\"]*\"" src/nhandu/__init__.py | cut -d'"' -f2); \
	echo "==> Current version: $$CURRENT"; \
	IFS='.' read -r major minor patch <<< "$$CURRENT"; \
	if [ "$(TYPE)" = "major" ]; then NEW="$$((major + 1)).0.0"; \
	elif [ "$(TYPE)" = "minor" ]; then NEW="$$major.$$((minor + 1)).0"; \
	elif [ "$(TYPE)" = "patch" ]; then NEW="$$major.$$minor.$$((patch + 1))"; \
	else echo "Error: TYPE must be patch, minor, or major"; exit 1; fi; \
	echo "==> Bumping $(TYPE) version to $$NEW..."; \
	sed -i "s/__version__ = \"$$CURRENT\"/__version__ = \"$$NEW\"/" src/nhandu/__init__.py; \
	echo "⚠️  Please update CHANGELOG.md manually before committing!"; \
	read -p "Press Enter to commit and tag, or Ctrl+C to cancel..." response; \
	git add src/nhandu/__init__.py; \
	git commit -m "chore: bump version to $$NEW"; \
	git tag -a "v$$NEW" -m "Release v$$NEW"; \
	echo "✓ Version bumped to $$NEW and tagged!"

build:
	python -m build

build-release: clean lint test build
	@echo "✓ Release build complete!"
	@ls -lh dist/

docs:
	@for tutorial in docs/*.md docs/*.py; do \
		[ -e "$$tutorial" ] || continue; \
		case "$$tutorial" in \
			*.out|*.html|*_executed.md) continue ;; \
		esac; \
		echo "Processing $$(basename "$$tutorial")..."; \
		python -m nhandu "$$tutorial" --format markdown -o "$$tutorial.out" || exit 1; \
		python -m nhandu "$$tutorial" --format html -o "$$tutorial.html" || exit 1; \
	done

docs-clean:
	rm -f docs/*.out docs/*.html
	rm -rf nhandu_output/

clean: docs-clean
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

all: lint test