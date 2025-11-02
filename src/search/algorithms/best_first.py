from .graph_search import GraphSearch
from search import Graph, Path


class BestFirst(GraphSearch):
    def search(self, graph: Graph, start: str, goal: str) -> Path:
        start_node = graph.get_node(start)
        goal_node = graph.get_node(goal)

        if not start_node or not goal_node:
            return Path([])

        # frontier: (útvonal, heurisztika)
        frontier: list[tuple[Path, int]] = [
            (Path([start_node]), start_node.heuristic) #kezdőérték
        ]
        explored: set[str] = set()

        while frontier:
            path, _ = frontier.pop(0)
            current = path.get_last()

            # ha már jártunk itt kihagyjuk
            if current.name in explored:
                continue
            explored.add(current.name)

            # cél?
            if current == goal_node:
                return path

            # új utakat nézünk generated<neightbor-ok majd a generated > frontiner majd fortiner rendezés.
            generated: list[tuple[Path, int]] = []
            for neighbor in sorted(current.get_neighbors(), key=lambda n: n.name):
                if neighbor not in path.get_nodes():
                    new_path = Path(path)
                    new_path.add_node(neighbor, 0)
                    generated.append((new_path, neighbor.heuristic))

            frontier = generated + frontier

            frontier.sort(key=lambda p: (p[1], p[0].get_last().name)) #heurisztika, majd név szerint rendezés

        return Path([])
