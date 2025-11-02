# AI Agent Instructions for Graph Search Project

## Project Overview
This is an educational project implementing various graph search algorithms in Python. The project provides a framework for implementing and testing different search strategies on graph structures.

## Core Components

### Data Structures (`src/search/graph.py`)
- `Node`: Represents graph vertices with name, edges, and heuristic values
- `Edge`: Represents weighted connections between nodes
- `Path`: Manages sequences of nodes with total path length
- `Graph`: Contains the graph structure with methods for node/edge management

### Search Algorithms (`src/search/algorithms/`)
- Each algorithm inherits from `GraphSearch` base class
- Must implement `search(graph: Graph, start: str, goal: str) -> Path`
- Available implementations include:
  - A* Search (`astar.py`)
  - Beam Search (`beam.py`)
  - Best-First Search (`best_first.py`)
  - BFS (`bfs.py`)
  - Branch and Bound (`branch_and_bound.py`)
  - DFS (`dfs.py`)
  - Hill Climbing (`hill_climbing.py`)

## Development Workflow

### Testing
1. Tests are defined in `tests/test_graph_search.py`
2. Test data is stored in `tests/resources/graphs.json`
3. Run tests using pytest:
   ```
   python -m pytest
   ```

### Adding New Algorithms
1. Create new file in `src/search/algorithms/`
2. Inherit from `GraphSearch` base class
3. Implement `search()` method
4. Register algorithm in `tests/algorithm_registry.py`

## Project Conventions
- Python ≥ 3.10 required
- Type hints are used throughout the codebase
- Graph node names are strings
- All paths must be valid sequences of connected nodes
- Test graphs are defined in JSON format with:
  - Nodes list
  - Edges list (with weights)
  - Optional heuristic values
  - Expected paths for each algorithm

## Common Patterns
- Use `graph.get_node(name)` to retrieve nodes by name
- Create paths using `Path(nodes_list)` or incrementally with `add_node()`
- Access a node's neighbors via `node.get_neighbors()`
- Compare paths using `==` operator (compares last node and total length)