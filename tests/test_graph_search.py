import json
import pytest
from pathlib import Path

from search.graph import Graph, Node, Path as GraphPath

from .algorithm_registry import get_algorithm

results = {} # tesztreredmények gyűjtélse

def load_graph_test_data():
    file_path = Path(__file__).parent / "resources" / "graphs.json"
    with file_path.open() as f:
        return json.load(f)  
    

def generate_test_cases():
    """Flatten (graph_id, algorithm_name, graph_data) triplets and IDs."""
    cases = []
    ids = []
    for graph_data in load_graph_test_data():
        graph_id = graph_data["graphId"]
        for algorithm_name in graph_data["expectedPaths"].keys():
            name = algorithm_name.replace("*", "star")
            cases.append((graph_id, algorithm_name, graph_data))
            ids.append(f"{graph_id} {name}")
    return cases, ids


cases, ids = generate_test_cases()


@pytest.mark.parametrize("graph_id, algorithm_name, graph_data", cases, ids=ids)
def test_graph_search_algorithms(graph_id, algorithm_name, graph_data):
    graph = Graph()
    for node in graph_data["nodes"]:
        graph.add_node(Node(node))
    for edge in graph_data["edges"]:
        graph.add_edge(edge["source"], edge["target"], edge["weight"])

    if "heuristic" in graph_data and graph_data["heuristic"] is not None:
        graph.set_heuristics(graph_data["heuristic"])

    expected_path_str = graph_data["expectedPaths"][algorithm_name]
    expected_nodes = [graph.get_node(ch) for ch in expected_path_str]
    expected_path = GraphPath(expected_nodes)

    algorithm = get_algorithm(algorithm_name)
    if algorithm is None:
        pytest.fail(f"Algorithm not found: {algorithm_name}")

    result_path = algorithm.search(graph, graph_data["start"], graph_data["goal"])

    # Eredmények mentése a futás közben
    results.setdefault(graph_id, {})[algorithm_name] = [
        n.name for n in result_path.get_nodes()
    ]

    assert expected_path == result_path, (
        f"Algorithm failed: {algorithm_name} on graph: {graph_id}\n"
        f"result: {result_path}, length: {result_path.length} \nexpected: {expected_path}, length: {expected_path.length}"
    )
    
