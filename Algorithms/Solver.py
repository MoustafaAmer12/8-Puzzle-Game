class Solver:
    def __init__(self, initial_state :str):
        self.initial_state = initial_state
        self.steps = list()

    def check_solvable(self):
        count = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if (self.initial_state[i] > self.initial_state[j] and
                    self.initial_state[j] != '0' and
                    self.initial_state[i] != '0'):
                    count += count
        return (count % 2 == 0)

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