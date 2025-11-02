from .graph_search import GraphSearch
from search import Graph, Path

#MEGVOLT
class BFS(GraphSearch):
    def search(self, graph: Graph, start: str, goal: str) -> Path:
        queue = [Path([graph.get_node(start)])]

        while queue:
            path = queue.pop(0)
            node = path.get_last()
            if node.name == goal:
                return path
            
            new_paths: list[Path] = []
            for neighbor in node.get_neighbors():
                if neighbor not in path.get_nodes():
                    new_path = Path(path)
                    new_path.get_nodes().append(neighbor)
                    new_paths.append(new_path)
            for path in sorted(new_paths):
                queue.append(path)

        return Path([])  # return empty path if not found