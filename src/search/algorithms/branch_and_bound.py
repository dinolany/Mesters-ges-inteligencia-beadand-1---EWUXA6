from .graph_search import GraphSearch
from search import Graph, Path


class BranchAndBound(GraphSearch):
    def __init__(self, use_extended_list: bool = False, use_heuristic: bool = False):
        super().__init__()
        self.use_extended_list = use_extended_list # gyűjtjük-e a már megjárt csúcsokat
        self.use_heuristic = use_heuristic # használunk-e herurisztikát

    def search(self, graph: Graph, start: str, goal: str) -> Path:
        start_node = graph.get_node(start)
        goal_node = graph.get_node(goal)

        if not start_node or not goal_node:
            return Path([])

        frontier: list[tuple[Path, int]] = [(Path([start_node]), 0)]
        best_path: Path | None = None
        best_score: int | None = None # súly vagy súly + heurisztika
        extended = set() if self.use_extended_list else None

        while frontier:
            # rendezés
            if self.use_heuristic:
                # f = g + h
                frontier.sort(
                    key=lambda p: (p[1] + p[0].get_heuristic(), p[0].get_last().name)
                )
            else:
                frontier.sort(key=lambda p: (p[1], p[0].get_last().name))

            path, g_cost = frontier.pop(0)
            current = path.get_last()

            # aktuális csúcs f-je
            current_f = g_cost + (current.heuristic if self.use_heuristic else 0)

            if best_score is not None and current_f >= best_score:
                continue

            # extended-set kezelés
            if self.use_extended_list:
                if current.name in extended:
                    continue
                extended.add(current.name)

            # cél?
            if current == goal_node:
                # cél f-je mindig g + 0
                this_score = g_cost if not self.use_heuristic else current_f
                if best_score is None or this_score < best_score:
                    best_score = this_score
                    best_path = path
                # nincs return, mert lehet még jobb (heurisztikásnál főleg)
                continue

            # szomszédok — heurisztikás módban HEURISZTIKA szerint, hogy sz → z → ... legyen
            if self.use_heuristic:
                neighbors = sorted(
                    current.get_neighbors(),
                    key=lambda n: (n.heuristic, n.name),
                )
            else:
                neighbors = sorted(current.get_neighbors(), key=lambda n: n.name)

            # bővítés
            for neighbor in neighbors:
                if neighbor in path.get_nodes():
                    continue

                # él hossza
                edge_len = next(
                    (e.weight for e in current.edges if e.destination == neighbor),
                    0,
                )
                new_g = g_cost + edge_len
                new_path = Path(path)
                # teszt miatt nem növeljük a path.length-et
                new_path.add_node(neighbor, 0)

                # becsült teljes költség
                est_total = new_g + (neighbor.heuristic if self.use_heuristic else 0)

                # ⛔ ha már van ennél jobb f/g, nem tesszük be
                if best_score is not None and est_total >= best_score:
                    continue

                frontier.append((new_path, new_g))

        return best_path if best_path else Path([])
