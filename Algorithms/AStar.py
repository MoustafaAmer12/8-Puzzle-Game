import time
from math import sqrt
from queue import heappop, heappush
from Algorithms.Solver import Solver

class Heuristic:
    def calculate(self, state):
        raise NotImplementedError("Heuristic strategy must implement the calculate method.")

class ManhattanDistance(Heuristic):
    def calculate(self, state):
        distance = 0
        goal_positions = {int(val): (i // 3, i % 3) for i, val in enumerate("012345678")}
        s = f"{state:09d}"

        for i, char in enumerate(s):
            if char != "0":
                current_pos = (i // 3, i % 3)
                goal_pos = goal_positions[int(char)]
                distance += abs(current_pos[0] - goal_pos[0]) + abs(current_pos[1] - goal_pos[1])

        return distance
    
class EuclideanDistance(Heuristic):
    def calculate(self, state):
        distance = 0
        goal_positions = {int(val): (i // 3, i % 3) for i, val in enumerate("012345678")}
        s = f"{state:09d}"

        for i, char in enumerate(s):
            if char != "0":
                current_pos = (i // 3, i % 3)
                goal_pos = goal_positions[int(char)]
                distance += sqrt((current_pos[0] - goal_pos[0])**2 + (current_pos[1] - goal_pos[1])**2)

        return distance
    


class AStar(Solver):
    def __init__(self, initial_state, heuristic: Heuristic, parent=None, move=None, depth=0, cost=0):
        super().__init__(initial_state)
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic


    def __lt__(self, other):
        return self.cost < other.cost
    
    def __eq__(self, other):
        return self.initial_state == other.initial_state
    def __gt__(self, other):
        return self.cost > other.cost

    def solve(self):
        if not self.check_solvable():
            return None

        print("Solving using A*...")
        start_time = time.time()
        priority_queue = []
        visited = {}
        initial_cost = self.heuristic.calculate(int(self.initial_state))
        heappush(priority_queue, (initial_cost, AStar(int(self.initial_state), self.heuristic)))
        visited[int(self.initial_state)] = initial_cost

        num_expanded = 0
        max_depth = 0

        while priority_queue:
            _, current_node = heappop(priority_queue)
            num_expanded += 1
            max_depth = max(max_depth, current_node.depth)
            

            if super().GoalTest(current_node.initial_state):
                end_time = time.time()
                solution_path = current_node.get_path()
                traced_path = current_node.trace_path()
                solution_path.insert(0, str(traced_path[0]).find('0'))
                return self.map(traced_path), self.map_path(solution_path) , len(solution_path) - 1, num_expanded, max_depth, end_time - start_time
                # return self.map(traced_path), len(solution_path), num_expanded, max_depth, round(end_time - start_time, 4)

            
            for move, initial_state in current_node.get_neighbors():
                new_depth = current_node.depth + 1
                new_cost = new_depth + self.heuristic.calculate(initial_state)
                if initial_state not in visited or new_cost < visited[initial_state]:
                    visited[initial_state] = new_cost
                    heappush(priority_queue, (new_cost, AStar(initial_state, self.heuristic, current_node, move, new_depth, new_cost)))

        return None
    

# # Example usage:
if __name__ == "__main__":
    initial_state = "123804765"  # Initial state as a string
    # Choose heuristic
    heuristic_strategy = ManhattanDistance()  # Use ManhattanDistance or EuclideanDistance()

    # heuristic_strategy = EuclideanDistance()
    goal_state = "281043765"
    solver = AStar(initial_state, heuristic=heuristic_strategy)
    solver.set_goal_state(int(goal_state))
    result = solver.solve()

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
