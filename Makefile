.PHONY: help install install-dev test lint format examples clean-examples clean all

help:
	@echo "Available commands:"
	@echo "  make install        Install nhandu in production mode"
	@echo "  make install-dev    Install nhandu with dev and test dependencies"
	@echo "  make test           Run tests with coverage"
	@echo "  make lint           Run mypy and ruff checks"
	@echo "  make format         Format code with ruff"
	@echo "  make examples       Run all example files and generate outputs"
	@echo "  make clean-examples Remove generated example outputs"
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

examples:
	@for example in examples/*.md examples/*.py; do \
		[ -e "$$example" ] || continue; \
		case "$$example" in \
			*.out|*.html|*_executed.md) continue ;; \
		esac; \
		echo "Processing $$(basename "$$example")..."; \
		python -m nhandu "$$example" --format markdown -o "$$example.out" || exit 1; \
		python -m nhandu "$$example" --format html -o "$$example.html" || exit 1; \
	done

clean-examples:
	rm -f examples/*.out examples/*.html
	rm -rf nhandu_output/

clean: clean-examples
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

all: lint test