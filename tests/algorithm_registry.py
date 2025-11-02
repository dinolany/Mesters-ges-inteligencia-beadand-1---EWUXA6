from search.algorithms import DFS, BFS, HillClimbing, Beam, BestFirst, BranchAndBound, AStar

ALGORITHMS = {
    "dfs": DFS(),
    "bfs": BFS(),
    "hill-climbing": HillClimbing(),
    "beam": Beam(2),
    "best-first": BestFirst(),
    "branch-and-bound": BranchAndBound(),
    "branch-and-bound-heuristic": BranchAndBound(use_heuristic=True),
    "branch-and-bound-extended-set": BranchAndBound(use_extended_list=True),
    "A*": AStar()
}

def get_algorithm(name: str):
    try:
        return ALGORITHMS[name]
    except KeyError:
        raise ValueError(f"Algorithm not found: {name}")