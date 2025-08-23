.PHONY: help install dev test lint format type-check clean build publish pre-commit

help:
	@echo "Available commands:"
	@echo "  make install      Install the package in production mode"
	@echo "  make dev          Install the package in development mode with all dev dependencies"
	@echo "  make test         Run tests with coverage"
	@echo "  make lint         Run linting checks"
	@echo "  make format       Format code with black and ruff"
	@echo "  make type-check   Run type checking with mypy"
	@echo "  make clean        Remove build artifacts and cache files"
	@echo "  make build        Build distribution packages"
	@echo "  make publish      Publish to PyPI (requires credentials)"
	@echo "  make pre-commit   Run pre-commit hooks on all files"

install:
	uv pip install -e .

dev:
	uv pip install -e ".[dev]"
	pre-commit install

test:
	uv run pytest tests/ -v --cov=chuk_term --cov-report=term-missing --cov-report=html

lint:
	uv run ruff check src/ tests/
	uv run black --check src/ tests/

format:
	uv run ruff check --fix src/ tests/
	uv run black src/ tests/

type-check:
	uv run mypy src/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	uv build

publish: build
	uv publish

pre-commit:
	pre-commit run --all-files

check: lint type-check test
	@echo "All checks passed!"