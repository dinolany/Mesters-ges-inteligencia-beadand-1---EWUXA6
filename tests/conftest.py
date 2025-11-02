# tests/conftest.py
import json
from pathlib import Path

def pytest_sessionfinish(session, exitstatus):
    """
    Pytest futás végén – HA elérhető a tests.test_graph_search.results –
    akkor kiírjuk a results.json-t. Ha nem elérhető, csendben továbblépünk.
    """
    try:
        # ha az én tesztemmel tesztelünk
        from .test_graph_search import results
    except Exception:
        # ha a tanár által megadott teszttel futtatunk, ahol nincs results
        return

    results_file = Path(__file__).parent / "results.json"
    with results_file.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Eredmények mentve ide: {results_file}")