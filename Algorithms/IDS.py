import time
from Algorithms.Solver import Solver
class IDS(Solver):
    def __init__(self, initial_state: str):
        super().__init__(initial_state)
        self.expandedNodes=0
        self.startTime=0
        self.endTime=0
    
    def output_path(self, states):
        indices = []
        for state in states:
            indices.append(state.find('0'))
        return indices
    
    def helper(self, Max):
        parent = {}    # parent map to store parent, child relationships
        DepthMap = {}  # Depth map

        frontier = []  # frontier stack
        explored = set()  # explored set
        frontier.append(int(self.initial_state))  # initial state
        parent[int(self.initial_state)] = -1
        DepthMap[int(self.initial_state)] = 0


        while frontier:

            current = frontier.pop()
            explored.add(current)
            self.expandedNodes=self.expandedNodes+1



            if (self.GoalTest(current)):
                ans = []
                while (parent[current] != -1):
                    ans.append(current)
                    current = parent[current]
                ans.append(current)
                ans.reverse()
                self.endTime=time.time()
                req = self.map(ans)
                path = self.map_path(self.output_path(req))

                return req, path, len(ans)-1,self.expandedNodes,Max,round(self.endTime-self.startTime, 4)

            if (DepthMap[current] >= Max):
                continue

            Stringified_State = str(current)
            if Stringified_State.find('0') == -1:
                Stringified_State = '0' + Stringified_State

            index = Stringified_State.find('0')
            children = self.generateChildren(Stringified_State, index)

            for child in children:

                if int(child) in explored and DepthMap[current]+1>DepthMap[int(child)]:
                    continue
                if int(child) in frontier and DepthMap[current]+1>DepthMap[int(child)]:
                    continue
                else:
                   DepthMap[int(child)] = DepthMap[int(current)] + 1
                   parent[int(child)] = current
                   frontier.append(int(child))

        return "Failure"


    def solve(self):
        if not self.check_solvable():
            return None
        
        print("Solving using IDS ...")
        self.startTime=time.time()
        x=0
        while(x<100):

           data=self.helper(x)
           if(data!="Failure"):
               return data
           x=x+1

if __name__ == "__main__":
    def run_solver(solver: Solver):
        result = solver.solve()
        print(result)
    
    dfs_solver = IDS("718654230")
    run_solver(dfs_solver)  # Example initial state
