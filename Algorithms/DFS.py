import time

from Algorithms.Solver import Solver
class DFS(Solver):
    # initializing parameters of DFS
    def __init__(self, initial_state: str):
        super().__init__(initial_state)
        self.parent={}   # parent map to store parent, child relationships
        self.maxDepth=0   # getting Max Depth of search (m)
        self.expandedNodes=0   # counter for expanded nodes
        self.DepthMap={}       # depth map storing node , Depth relationships

    def solve(self):

        startTime=time.time()
        frontier=[]
        explored=set()
        frontier.append(int(self.initial_state))
        self.parent[int(self.initial_state)]=-1
        self.DepthMap[int(self.initial_state)]=0


        while frontier:

            current=frontier.pop()
            explored.add(current)
            if(self.DepthMap[current]>self.maxDepth):    #updating max depth
                self.maxDepth=self.DepthMap[current]

            self.expandedNodes=self.expandedNodes+1

            if(super().GoalTest(current)):    #Goal test
                ans=[]
                while(self.parent[current]!= -1):    # constructing path
                    ans.append(current)
                    current=self.parent[current]
                ans.append(current)    #append start state
                ans.reverse()          # reverse path to get it in right order
                endTime=time.time()
                return self.map(ans), len(ans)-1, self.expandedNodes, self.maxDepth, round(endTime-startTime, 4)   # returning data



            Stringified_State=str(current)     # stringifiy state
            if(Stringified_State.find('0')==-1):         # solving problem of missing zero
                Stringified_State='0'+Stringified_State

            index=Stringified_State.find('0')
            children=super().generateChildren(Stringified_State,index)   # generating children

            for child in children:
                if (int(child) in explored):
                    continue
                elif (int(child) in frontier):
                    continue
                else:
                    self.DepthMap[int(child)]=self.DepthMap[int(current)]+1   #depth of child
                    self.parent[int(child)]=current    #setting parent
                    frontier.append(int(child))        # appending to frontier



if __name__ == "__main__":
    def run_solver(solver: Solver):
        result = solver.solve()
        print(result)

    dfs_solver = DFS("718654230")
    run_solver(dfs_solver)  # Example initial state
