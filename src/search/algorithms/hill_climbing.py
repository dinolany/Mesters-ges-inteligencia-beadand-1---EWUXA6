from .graph_search import GraphSearch
from search import Graph, Path

class HillClimbing(GraphSearch):
    def search(self, graph: Graph, start: str, goal: str) -> Path:
        start_node = graph.get_node(start)
        goal_node = graph.get_node(goal)

        if not start_node or not goal_node:
            return Path([])

        path = Path([start_node])
        current_node = start_node

        while current_node != goal_node:
            neighbors = [
                n for n in current_node.get_neighbors()
                if n not in path.get_nodes()  # ne menjünk vissza
            ]
            
            if not neighbors:
                # zsákutca, nem lehet továbbmenni
                return Path([])

            # válasszuk a legjobb heurisztikájú szomszédot
            neighbors.sort(key=lambda n: getattr(n, "heuristic", 0))
            current_node = neighbors[0]

            path.add_node(current_node, 0)

        return path
