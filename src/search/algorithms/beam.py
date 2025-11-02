from .graph_search import GraphSearch
from search import Graph, Path


class Beam(GraphSearch):
    def __init__(self, beam_width: int = 2):
        self.beam_width = beam_width

    def search(self, graph: Graph, start: str, goal: str) -> Path:
        start_node = graph.get_node(start)
        goal_node = graph.get_node(goal)

        # induló nyaláb
        beam: list[Path] = [Path([start_node])]

        if start_node == goal_node:
            return beam[0]

        while beam:
            generated: list[Path] = []

            # keressük a szomszédokat
            for path in beam:
                last = path.get_last()
                for edge in last.edges:
                    neighbor = edge.destination

                    # vótmá
                    if neighbor in path.get_nodes():
                        continue

                    new_path = Path(path)
                    new_path.get_nodes().append(neighbor)

                    # cél?
                    if neighbor == goal_node:
                        return new_path

                    generated.append(new_path)

            if not generated:
                return Path([])

            # randezzük heurisztika majd név szerint és a legjobb 2-t tarjuk meg (a beam width)
            generated.sort(key=lambda p: (p.get_last().heuristic, p.get_last().name))
            beam = generated[:self.beam_width]

        return Path([])
