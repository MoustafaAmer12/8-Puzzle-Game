class Solver:
    GOAL_STATE = 12345678

    def __init__(self, initial_state :str):
        self.initial_state = initial_state


    def check_solvable(self):
        count = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if (self.initial_state[i] > self.initial_state[j] and
                    self.initial_state[j] != '0' and
                    self.initial_state[i] != '0'):
                    count += 1
        return (count % 2 == 0)

    @classmethod
    def set_goal_state(cls, new_goal):
        """Class method to set a new global goal state."""
        cls.GOAL_STATE = new_goal

    @classmethod
    def get_goal_state(cls):
        """Class method to get the current global goal state."""
        return cls.GOAL_STATE

    # To test goal in solution
    def GoalTest(self,state):
        return state == self.GOAL_STATE
    # To generate children of a state
    def generateChildren(self,stringified_state, index):
        up, down, left, right = index - 3, index + 3, index - 1, index + 1
        children = []

        # Convert the string to a list to allow modifications
        state_list = list(stringified_state)

        # moving up
        if up >= 0:
            new_state = state_list[:]
            new_state[index], new_state[up] = new_state[up], '0'
            children.append(''.join(new_state))

        # Move left
        if left >= 0 and index % 3 != 0:  # mod checks for points on the corner
            new_state = state_list[:]
            new_state[index], new_state[left] = new_state[left], '0'
            children.append(''.join(new_state))

        # Move right
        if right <= 8 and (index + 1) % 3 != 0:
            new_state = state_list[:]
            new_state[index], new_state[right] = new_state[right], '0'
            children.append(''.join(new_state))

            # moving down
        if down <= 8:
            new_state = state_list[:]
            new_state[index], new_state[down] = new_state[down], '0'
            children.append(''.join(new_state))

        return children

    def map(self, states):
        new_states = []
        for state in states:
            if type(state) is int:
                new_state = str(state)
                if len(new_state) != 9:
                    new_state = '0' + new_state
                new_states.append(new_state)
        return new_states
                

    # To Be Overridden
    def solve(self):
        pass

    def get_path(self):
        """Backtrack to get the path of moves from the initial state to this state."""
        path = []
        node = self
        while node.parent is not None:
            path.append(node.move)
            node = node.parent
        return path[::-1]

    def get_neighbors(self):
        """Generate possible moves and resulting states from the current state."""
        neighbors = []
        s = str(self.initial_state)
        zero_index = s.find("0")
        if zero_index == -1:
            s = "0" + s
            zero_index = 0
        moves = {
            0: [1, 3],    1: [0, 2, 4],    2: [1, 5],
            3: [0, 4, 6], 4: [1, 3, 5, 7], 5: [2, 4, 8],
            6: [3, 7],    7: [4, 6, 8],    8: [5, 7]
        }

        for pos in moves[zero_index]:
            new_state = list(s)
            new_state[zero_index], new_state[pos] = new_state[pos], new_state[zero_index]
            neighbors.append((pos, int("".join(new_state))))

        return neighbors
    


    def trace_path(self):
        """Trace the path from the start to the given node."""
        path = []
        node = self 
        while node is not None:
            path.append(node.initial_state)
            node = node.parent
        return path[::-1] 



    # Check If Unified or Not
    def pipeline(self):
        if not self.check_solvable():
            return -1
        self.solve()
        # self.map()