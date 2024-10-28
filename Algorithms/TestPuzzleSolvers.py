import unittest
from BFS import BFS
from AStar import AStar, EuclideanDistance, ManhattanDistance
class TestPuzzleSolvers(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            ("123456780", "123456780", 0),
            ("123804765", "281043765", 9),
            ("123804765", "281463075", 12),
            ("134805726", "123804765", 6),
            ("231708654", "123804765", 14),
            ("231804765", "123804765", 16),
            ("123804765", "231804765", 16),
            ("283104765", "123804765", 4),
            ("876105234", "123804765", 28),
            ("867254301", "123456780", 31),
            ("647850321", "123456780", 31),
            ("123804765", "567408321", 30),
            ("806547231", "012345678", 31),
            ("641302758", "012345678", 14),
            ("158327064", "012345678", 12),
        ]

    def test_bfs(self):
        for initial_state, goal_state, expected_moves in self.test_cases:
            bfs_solver = BFS(initial_state)
            bfs_solver.set_goal_state(int(goal_state))
            result = bfs_solver.solve()
            if result:
                traced_path, solution_path, path_length, num_expanded, max_depth, time_taken = result
                self.assertEqual(path_length, expected_moves, f"BFS failed for initial: {initial_state} with goal: {goal_state}. Expected {expected_moves}, got {path_length}.")
            else:
                self.fail(f"BFS failed for initial: {initial_state} with goal: {goal_state}. No solution found.")
        pass


    def test_a_star(self):
        euclidean_heuristic = EuclideanDistance()
        manhattan_heuristic = ManhattanDistance()
        for initial_state, goal_state, expected_moves in self.test_cases:
            solver = AStar(initial_state, heuristic=manhattan_heuristic)
            solver.set_goal_state(int(goal_state))
            result = solver.solve()
            if result:
                traced_path, solution_path, path_length, num_expanded, max_depth, time_taken = result
                self.assertEqual(path_length, expected_moves, f"A* failed for initial: {initial_state} with goal: {goal_state}. Expected {expected_moves}, got {path_length}.")
            else:
                self.fail(f"A* failed for initial: {initial_state} with goal: {goal_state}. No solution found.")



if __name__ == '__main__':
    unittest.main()
