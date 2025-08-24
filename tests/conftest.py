"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_config_file(tmp_path):
    """Create a temporary configuration file."""
    config_file = tmp_path / "config.yaml"
    config_file.write_text(
        """
terminal:
  width: 80
  height: 24
  color_scheme: "default"
"""
    )
    return config_file


@pytest.fixture(autouse=True)
def add_src_to_path():
    """Add src directory to Python path for testing."""
    src_path = Path(__file__).parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    yield
    if str(src_path) in sys.path:
        sys.path.remove(str(src_path))
