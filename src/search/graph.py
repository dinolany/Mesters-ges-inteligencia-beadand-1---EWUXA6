from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass(frozen=True)
class Edge:
    destination: Node
    weight: float

    def __str__(self) -> str:
        return f"[{self.destination} {self.weight}]"

@dataclass(order=True)
class Node:
    name: str
    edges: List[Edge] = field(default_factory=list)
    heuristic: int = 0

    def get_neighbors(self) -> List[Node]:
        return [edge.destination for edge in self.edges]

    def set_edges(self, edges: List[Edge]) -> None:
        self.edges = edges

    def add_neighbor(self, neighbor: Node, distance: int = 0) -> None:
        self.edges.append(Edge(destination=neighbor, weight=distance))

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def __str__(self) -> str:
        neighbors = [edge.destination.name for edge in self.edges]
        return f"Node {self.name}[neighbors={neighbors}, heuristic={self.heuristic}]"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False
        return self.name == other.name

@dataclass
class Path:
    nodes: List[Node] = field(default_factory=list)
    length: int = 0

    def __init__(self, other: List[Node] | Path | None = None, length: int = 0):
        if isinstance(other, Path):
            self.nodes = other.nodes.copy()
            self.length = other.length
        elif isinstance(other, list):
            self.nodes = list(other)
            self.length = length
        else:
            self.nodes = []
            self.length = length

    def add_length(self, length: int) -> None:
        self.length += length

    def get_nodes(self) -> List[Node]:
        return self.nodes

    def set_nodes(self, nodes: List[Node]) -> None:
        self.nodes = list(nodes)

    def add_node(self, node: Node, length: int = 0) -> None:
        self.nodes.append(node)
        self.length += length

    def get_last(self) -> Node:
        return self.nodes[-1]

    def get_heuristic(self) -> int:
        return self.get_last().heuristic

    def __str__(self) -> str:
        return f"({''.join(node.name for node in self.nodes)})"

    # --- Comparison methods ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.get_last().name == other.get_last().name and self.length == other.length

    def __lt__(self, other: Path) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return self.get_last().name < other.get_last().name

    def __gt__(self, other: Path) -> bool:
        if not isinstance(other, Path):
            return NotImplemented
        return other < self

    def __le__(self, other: Path) -> bool:
        return self == other or self < other

    def __ge__(self, other: Path) -> bool:
        return self == other or self > other

@dataclass
class Graph:
    nodes: Dict[str, Node] = field(default_factory=dict)

    def get_node(self, name: str) -> Node | None:
        return self.nodes.get(name)

    def add_node(self, node: Node) -> None:
        self.nodes[node.name] = node

    def add_edge(self, a: str | Node, b: str | Node, length: int = 0) -> None:
        """Adds an undirected edge between nodes a and b, by name or by reference."""
        # Convert names to Node objects if needed
        node_a = self.nodes[a] if isinstance(a, str) else a
        node_b = self.nodes[b] if isinstance(b, str) else b
        node_a.add_neighbor(node_b, length)
        node_b.add_neighbor(node_a, length)

    def set_heuristics(self, heuristics: Dict[str, int]) -> None:
        """Set heuristic values for each node."""
        for name, value in heuristics.items():
            if name in self.nodes:
                self.nodes[name].heuristic = value

    def __str__(self) -> str:
        return f"Graph({', '.join(self.nodes.keys())})"