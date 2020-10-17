import numpy as np

dim = 8
grid = []
for row in range(dim):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(dim):
        grid[row].append(np.random.binomial(1, 0.5, 1))  # Append a cell
        if (row == column == dim - 1):
            grid[row][column] = 0
grid[0][0] = 0


class junct():
    def __init__(self, row, column, parent_S, parent_G):
        self.row = row
        self.column = column
        self.parent_S = parent_S
        self.parent_G = parent_G

    def __eq__(self, other):
        return (self.row == other.row and self.column == other.column)

    def bidirectional_bfs(self):
        def get_value(maze, a, b):
            return maze[a][b]

        def is_out_of_bounds(a, b, d):
            return (a < 0 or a >= dim) or (b < 0 or b >= d)

        grid = self.grid
        dim = len(grid)
        Q_start = []
        Q_goal = []
        visited = []
        start = junct(0, 0, None, None)
        goal = junct(dim - 1, dim - 1, None, None)
        Q_start.append(start)
        Q_goal.append(goal)
        visited.append(start)
        visited.append(goal)

        # beginning loop
        while (len(Q_start) > 0) and (len(Q_goal) > 0):
            # initializations
            current_S = Q_start[0]
            current_G = Q_goal[0]

            row_S = current_S.row
            column_S = current_S.column

            row_G = current_G.row
            column_G = current_G.column

            # some mechanics
            if len(Q_start) > 0:
                Q_start.pop(0)
            if len(Q_goal) > 0:
                Q_goal.pop(0)

            # in case the current node from starting is in the goal Queue
            if (current_S in Q_goal):
                # forming the path back to G
                current = current_S
                path_S = [current]
                while current.parent_S is not None:
                    path_S.append(current.parent_S)
                    current = current.parent_S
                path_S = [(item.row, item.column) for item in path_S]
                print(path_S)

            # in case the current node from goal is in the start Queue
            if (current_G in Q_start):
                # forming the path back to S
                current = current_G
                path_G = [current]
                while current.parent_S is not None:
                    path_G.append(current.parent_G)
                    current = current.parent_G
                path_G = [(item.row, item.column) for item in path_G]
                print(path_G)

            if (current_S in Q_goal) and (current_G in Q_start):
                path = [item for item in path_G for item in path_S]
                print(path)
                return path

            # enqueueing children from the start direction
            children_S = [junct(row_S + 1, column_S, current_S, None), junct(row_S - 1, column_S, current_S, None),
                          junct(row_S, column_S + 1, current_S, None), junct(row_S, column_S - 1, current_S, None)]
            for child in children_S:
                if not is_out_of_bounds(child.row, child.column, dim):
                    if child not in visited:
                        if get_value(grid, child.row, child.column) == 0:
                            Q_start.append(child)
                            visited.append(child)

            # enqueueing childen from the goal direction
            # enqueueing children from the start direction
            children_G = [junct(row_G + 1, column_G, None, current_G), junct(row_G - 1, column_G, None, current_G),
                          junct(row_G, column_G + 1, None, current_G), junct(row_G, column_G - 1, None, current_G)]
            for child in children_S:
                if not is_out_of_bounds(child.row, child.column, dim):
                    if child not in visited:
                        if get_value(grid, child.row, child.column) == 0:
                            Q_goal.append(child)
                            visited.append(child)

        print("No path")
        return []



