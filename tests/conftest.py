import pytest
import json
from pathlib import Path

from .test_graph_search import results


def pytest_sessionfinish(session, exitstatus):
    """
    Pytest futás végén automatikusan menti a results.json fájlt
    a tests/ mappába.
    """
    results_file = Path(__file__).parent / "results.json"
    with results_file.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Eredmények mentve ide: {results_file}")
