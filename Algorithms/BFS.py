import time
from collections import deque
from Algorithms.Solver import Solver

class BFS(Solver):
    def __init__(self, initial_state, parent=None, move=None, depth=0):
        super().__init__(initial_state)
        self.parent = parent
        self.move = move
        self.depth = depth
    

    def solve(self):
        """Perform BFS to find the solution path and calculate metrics."""
        start_time = time.time()

        queue = deque([BFS(int(self.initial_state))])
        visited = {int(self.initial_state)}
        num_expanded = 0
        max_depth = 0

        while queue:
            current_node = queue.popleft()
            num_expanded += 1
            max_depth = max(max_depth, current_node.depth)
            if super().GoalTest(current_node.initial_state):
                end_time = time.time()
                solution_path = current_node.get_path()
                traced_path = current_node.trace_path()
                # return traced_path, solution_path, len(solution_path), num_expanded, max_depth, end_time - start_time
                return self.map(traced_path), len(solution_path), num_expanded, max_depth, round(end_time - start_time, 4)
            
            for move, initial_state in current_node.get_neighbors():
                if initial_state not in visited:
                    visited.add(initial_state)
                    queue.append(BFS(initial_state, current_node, move, current_node.depth + 1))

        return None
            
if __name__ == "__main__":
    initial_state = "123456780"
    goal_state = "123456780"
    bfs_solver = BFS(initial_state)
    bfs_solver.set_goal_state(int(goal_state))
    result = bfs_solver.solve()


    if result:
        traced_path, solution_path, path_length, num_expanded, max_depth, time_taken = result

        print("Result Metrics:")
        print("Traced Path:", [node.initial_state for node in traced_path])
        print("Solution Path:", solution_path)
        print("Number of Steps:", path_length)
        print("Number of Expanded Nodes:", num_expanded)
        print("Max Depth Reached:", max_depth)
        print("Time Taken:", time_taken, "seconds")
    else:
        print("No solution found.")
