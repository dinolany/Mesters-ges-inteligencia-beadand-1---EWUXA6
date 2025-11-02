from __future__ import annotations
from abc import ABC, abstractmethod
from search import Graph, Path


class GraphSearch(ABC):
    """Abstract base class for graph search algorithms."""

    @abstractmethod
    def search(self, graph: Graph, start: str, goal: str) -> Path:
        """Perform a graph search and return the resulting Path."""
        pass
