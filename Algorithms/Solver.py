class Solver:
    def __init__(self, initial_state :str):
        self.initial_state = initial_state


    def check_solvable(self):
        count = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if (self.initial_state[i] > self.initial_state[j] and
                    self.initial_state[j] != '0' and
                    self.initial_state[i] != '0'):
                    count += count
        return (count % 2 == 0)

    # To test goal in solution
    def GoalTest(self,state):
        return state == 12345678
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

    def map(self):
        pass

    # To Be Overridden
    def solve(self):
        pass


    # Check If Unified or Not
    def pipeline(self):
        if not self.check_solvable():
            return -1
        self.solve()
        # self.map()