from .graph_search import GraphSearch
from search import Graph, Path


class AStar(GraphSearch):
    def search(self, graph: Graph, start: str, goal: str) -> Path:
        start_node = graph.get_node(start)
        goal_node = graph.get_node(goal)

        if not start_node or not goal_node:
            return Path([])

        # az út eddigi költsége
        g_cost: dict[str, int] = {start_node.name: 0}

        frontier: list[tuple[Path, int]] = [
            (Path([start_node]), start_node.heuristic)
        ]

        while frontier:
            # a legkisebb f-ű csúcs kiválasztása (f(becsültt költség)= tényleges költség(q_cost) + heurisztika)
            frontier.sort(key=lambda x: (x[1], x[0].get_last().name))
            path, _ = frontier.pop(0)
            current = path.get_last()

            # ha cél, kész
            if current == goal_node:
                return path

            # szomszédok bővítése 
            for edge in sorted(current.edges, key=lambda e: e.destination.name):
                neighbor = edge.destination
                tentative_g = g_cost[current.name] + edge.weight

                if neighbor.name in g_cost:
                    # annak vizsgálata hogy a jelenlegi útvonal olcsóbb-e mint a jelenlegi
                    if neighbor == goal_node and tentative_g < g_cost[neighbor.name]:
                        g_cost[neighbor.name] = tentative_g
                    else:
                        continue
                else:
                    g_cost[neighbor.name] = tentative_g

                # új útvonal felvétele 
                new_path = Path(path)
                new_path.add_node(neighbor, 0)

                f_score = g_cost[neighbor.name] + neighbor.heuristic
                frontier.append((new_path, f_score))

        return Path([])
