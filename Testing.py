import numpy as np

def generateGrid(dim, prob):
    # dim = 10
    grid = []
    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            grid[row].append(int(np.random.binomial(1, prob, 1)))  # Append a cell
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 1
    grid[dim - 1][dim - 1] = 1
    return grid



def mazeWithFire():
    # N = 100
    # successCount = 0
    # for _ in itertools.repeat(None, N):
    #     pathExists = simulate(10, 0.8)
    #     successCount = successCount + pathExists
    # print(successCount)
    dim = 10
    fillProb = 0.6
    fireprob = 0.5
    maze = generateGrid(dim, fillProb)
    visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    visited = [[True if b == 0 else False for b in i] for i in maze]
    print('visited')

mazeWithFire()