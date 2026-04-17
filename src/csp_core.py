class CSPSolver:
    def __init__(self,graph,colors):
        self.graph = graph
        self.colors = colors
        self.solution = {}
    
    def isValid(self,node,colors):
        for neighbor in self.graph[node]:
            if neighbor in self.solution and self.solution[neighbor] == colors:
                return False
        return True
    
    def get_unassigned_node(self):
        for node in self.graph:
            if node not in self.solution:
                return node
        return None

    def backTrack(self, depth=0):
        indent = "  " * depth

        if len(self.solution) == len(self.graph):
            print(indent + "DONE:", self.solution)
            return True

        node = self.get_unassigned_node()
        print(indent + f"Node: {node}")

        for color in self.colors:
            print(indent + f"Try {color}")

            if self.isValid(node, color):
                self.solution[node] = color

                if self.backTrack(depth + 1):
                    return True

                print(indent + f"Backtrack {node}")
                del self.solution[node]

        return False
        
    def solve(self):
        if self.backTrack():
            return self.solution
        return None

def solve_csp(graph, colors):
    solver = CSPSolver(graph, colors)
    return solver.solve()

#test code
# if __name__ == "__main__":
#     graph = {
#         "Hà Nội": ["Bắc Ninh", "Hưng Yên"],
#         "Bắc Ninh": ["Hà Nội"],
#         "Hưng Yên": ["Hà Nội"]
#     }

#     colors = ["Red", "Green"]

#     result = solve_csp(graph, colors)

#     print("\nKết quả cuối:", result)
#test push github
