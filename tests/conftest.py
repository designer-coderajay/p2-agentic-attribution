"""Shared fixtures. Seeds are pinned in every test that draws randomness, per
standing rule 10: no reported number depends on an unpinned seed."""
import os
import sys

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))


@pytest.fixture(scope="session")
def repo_root():
    return REPO
