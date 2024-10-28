from Algorithms.DFS import DFS
from Algorithms.BFS import BFS
from Algorithms.IDS import IDS
from Algorithms.AStar import AStar, ManhattanDistance, EuclideanDistance

class SolverFactory:
    def __init__(self, initialState):
        self.initialState = initialState
    
    def get_method(self, method:str):
        if method == "DFS":
            return DFS(self.initialState)
        elif method == "BFS":
            return BFS(self.initialState)
        elif method == "Iterative DFS":
            return IDS(self.initialState)
        elif method == "A* (Manhattan)":
            return AStar(self.initialState, heuristic=ManhattanDistance())
        elif method == "A* (Euclidean)":
            return AStar(self.initialState, heuristic=EuclideanDistance())