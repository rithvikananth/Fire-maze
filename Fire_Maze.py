__author__ = "Aravinda Reddy Dandu"

import copy
import itertools
from pprint import pprint
from random import randint
from collections import deque
import numpy as np


# Importing all the required libraries

# Function to generate grid given dimension and fill percentage(as probability). 0 is blocked cell. 1 is empty cell
def generateGrid(dim, prob):
    grid = []
    for row in range(dim):
        grid.append([])
        for column in range(dim):
            # Using numpy to get 0 or 1 from a binomial distribution with required probability
            grid[row].append(int(np.random.binomial(1, prob, 1)))
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 1
    grid[dim - 1][dim - 1] = 1
    return grid


# Defining a location class to store co-ordinates
class Location:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    # Overriding equals method to check equality of objects
    def __eq__(self, other):
        if isinstance(other, Location):
            return (self.x == other.x) and (self.y == self.y)
        return False


# Defining a QueueNode class to store location and distance from source
class QueuePoint:
    def __init__(self, pt: Location, dist: int):
        self.pt = pt
        self.dist = dist


# Defining a method to check if a given cell is valid in maze
def isCellValid(mat, row: int, col: int):
    return (row >= 0) and (row < len(mat)) and (col >= 0) and (col < len(mat[0]))


# Defining two dictionaries to facilitate 4-direction movement. Used for BFS and spreading fire
rowMov = [-1, 0, 0, 1]
colMov = [0, -1, 1, 0]


# Typical BFS method using Queue and exploration
def breadthFirstSearch(maze, source: Location, goal: Location):
    if maze[source.x][source.y] != 1 or maze[goal.x][goal.y] != 1:  # Return if source or dest is blocked. Never
        # happens as such maze won't be created. Just to generalize the method
        return -1
    q = deque()  # Using the queue functionality in Python
    # Defining a boolean array to store visited cells. Adding source to it
    visited = [[False for i in range(len(maze[0]))] for j in range(len(maze))]
    visited[source.x][source.y] = True
    s = QueuePoint(source, 0)
    # Initializing the queue by adding source
    q.append(s)
    while q:
        # Popping queue to get next cell in queue and checking if it's the goal point
        current = q.popleft()
        pt = current.pt
        if pt.x == goal.x and pt.y == goal.y:
            return current
        # Iterating four times for four directions defined above
        for i in range(4):
            row = pt.x + rowMov[i]
            col = pt.y + colMov[i]
            # Checking if cell in this direction is valid. If valid, adding it to the queue
            if isCellValid(maze, row, col) and maze[row][col] == 1 and not visited[row][col]:
                visited[row][col] = True
                AdjPoint = Location(row, col)
                # Setting the prev attribute to trace the path back from destination
                AdjPoint.prev = pt
                Adjcell = QueuePoint(AdjPoint, current.dist + 1)
                q.append(Adjcell)
    return -1  # Return -1 if goal is never reached and all cells are explored


# Method which uses BFS and gets a path from source to destination
def getSolution(source, dest, mat):
    # maze = [[1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    #        [0, 1, 1, 0, 1, 1, 1, 1, 0, 0],
    #        [1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
    #        [1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
    #        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    #        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    #        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    #        [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    #        [1, 1, 1, 1, 1, 0, 0, 0, 1, 1],
    #        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]]
    dim = len(mat)
    # Defining a out array which will have 1s stating the path. Only for visualization
    out = [[0 for col in range(dim)] for row in range(dim)]
    path = []
    out[source.x][source.y] = 1
    out[dest.x][dest.y] = 1
    # getting the destination node with it's prev attribute from BFS method
    node = breadthFirstSearch(mat, source, dest)
    if node == -1:
        print("Path doesn't exist")
        return 0
    elif node.dist != -1:
        print("Shortest Path is", node.dist)
    point = node.pt
    # Tracing back and making a path from source to destination
    while hasattr(point, 'prev'):
        pointN = Location(point.x, point.y)
        point = point.prev
        out[point.x][point.y] = 1
        path.append(pointN)
    path.append(Location(source.x, source.y))
    path = list(reversed(path))
    # pprint(out) # This will pretty print the array with 1s showing the path
    return path


# First strategy
def mazeWithFireNaive(dim, fillProb, fireprob):
    source = Location(0, 0)
    dest = Location(dim - 1, dim - 1)
    # Generating a maze using generateGrid method. This has to be the same for all the 10 iterations with random fire
    # locations
    cleanMaze = generateGrid(dim, fillProb)
    # Generating a solution using BFS method. This has to be the same for all the 10 iterations with random fire
    # locations
    solution = getSolution(source, dest, cleanMaze)
    if solution == 0:
        print('no solution')
    else:
        # Creating a boolean dim*dim array to store previous fire locations and blocked cells
        visited = [[True if b == 0 else False for b in i] for i in cleanMaze]
        visited[0][0] = True
        visited[dim - 1][dim - 1] = True
        count = 0
        for row in range(dim):
            for column in range(dim):
                if visited[row][column]:
                    count = count + 1
        mazeCount = []
        for _ in itertools.repeat(None, simulatonsPerMaze):
            maze = copy.deepcopy(cleanMaze)  # Creating a new instance of maze for every iteration and using it
            firecell = Location(randint(0, dim - 1), randint(0, dim - 1))  # Generating a random fire cell using
            # randint library
            flag = False  # Using this to break inner loop and continue if agent is dead
            # Checking if path exists from fire cell and source. Also checking if this fire cell is not used previously
            while visited[firecell.x][firecell.y] or (breadthFirstSearch(maze, Location(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
                count = count + 1
                if count == dim * dim:
                    # If all cells are visited, returning as no where to put fire
                    mazeCount.append('Nowhere to put fire')
                    return mazeCount
            # Flagging current fire cell as visited
            visited[firecell.x][firecell.y] = True
            # Using 3 as indicator to fire cell
            maze[firecell.x][firecell.y] = 3
            print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
            for point in solution:
                # Spreading fire with given probability
                maze = spreadFire(maze, fireprob, False)
                if maze[point.x][point.y] == 2:  # Dead if current cell catches fire
                    pprint(maze)
                    mazeCount.append('dead')
                    print('dead')
                    flag = True
                    break
            if flag:
                continue
            pprint(maze)
            mazeCount.append('alive')  # Alive if it reaches dest and points in solution are exhausted
            print('alive')
        return mazeCount


# Second strategy
def mazeWithFireRebuild(dim, fillProb, fireProb):
    # Using same variables as first strategy
    source = Location(0, 0)
    dest = Location(dim - 1, dim - 1)
    cleanMaze = generateGrid(dim, fillProb)
    initialsolution = getSolution(source, dest, cleanMaze)
    if initialsolution == 0:
        print('no solution')
    else:
        visited = [[True if b == 0 else False for b in i] for i in cleanMaze]
        visited[0][0] = True
        visited[dim - 1][dim - 1] = True
        count = 0
        for row in range(dim):
            for column in range(dim):
                if visited[row][column]:
                    count = count + 1
        mazeCount = []
        for _ in itertools.repeat(None, simulatonsPerMaze):
            maze = copy.deepcopy(cleanMaze)
            solution = copy.deepcopy(initialsolution)  # Required to clone the initial solution as it gets changed
            firecell = Location(randint(0, dim - 1), randint(0, dim - 1))  # Using same strategy as first to generate
            # random fire cell
            while visited[firecell.x][firecell.y] or (breadthFirstSearch(maze, Location(0, 0), firecell) == -1):
                visited[firecell.x][firecell.y] = True
                firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
                count = count + 1
                if count == dim * dim:
                    return 'Nowhere to put fire'
            visited[firecell.x][firecell.y] = True
            maze[firecell.x][firecell.y] = 3
            print('Fire cell location is (' + str(firecell.x) + ', ' + str(firecell.y) + ')')
            point = solution[1]
            while maze[point.x][point.y] != 2:
                maze = spreadFire(maze, fireProb, False)
                solution = getSolution(point, dest, maze)  # Getting a solution from current point to destination in
                # every iteration. This is the crucial change from first strategy
                if solution == 0:  # Dead if no solution from current point to dest
                    mazeCount.append('dead')
                    print('dead')
                    break
                point = solution[1]
                if point == dest:  # Alive if point is dest
                    pprint(maze)
                    mazeCount.append('alive')
                    print('alive')
                    break
        return mazeCount


# This is method to spread fire. 2 is the actual fire indicator. 3 is an intermediate to prevent fire from spreading
# in loops. 4 is to indicate fake fire(Used in third strategy). 5 is an intermediate state to prevent spreading of
# fake fire in loops.
def spreadFire(mat, fireprob, fake):
    dim = len(mat)
    # Changing all 2s to 3s to spread fire using actual indicators
    mat = [[3 if b == 2 else b for b in i] for i in mat]
    # Changing 4 to 5 to spread fake fire. 5 is to prevent spreading in loops
    mat = [[5 if b == 4 else b for b in i] for i in mat]
    for row in range(dim):
        for column in range(dim):
            pt = Location(row, column)
            firecount = 0
            for i in range(4):
                rowloc = pt.x + rowMov[i]
                colloc = pt.y + colMov[i]
                # Finding all neighbouring cells and checking for fire(indicated by 3)
                if isCellValid(mat, rowloc, colloc) and (mat[rowloc][colloc] == 3 or mat[rowloc][colloc] == 5):
                    firecount = firecount + 1
            prob = 1 - pow((1 - fireprob), firecount)  # Using the given prob function to determine fire probability
            check = int(np.random.binomial(1, prob, 1))
            if fake:
                if check == 1 and mat[row][column] == 1:
                    mat[row][column] = 4
            else:
                if check == 1 and mat[row][column] == 1:
                    mat[row][column] = 2
    # Reverting back to initial states after spreading fire
    mat = [[2 if b == 3 else b for b in i] for i in mat]
    mat = [[4 if b == 5 else b for b in i] for i in mat]
    return mat


# Driver method to test strategies
def test_strategies():
    # Defining a global simulations per maze variable
    global simulatonsPerMaze
    # N is number of iterations
    N = 10
    simulatonsPerMaze = 10
    # dim is maze dimension
    dim = 20
    # Maze free cell probability
    fillProb = 0.7
    # Dict to give CSV output
    storageDict = {}
    # Lopoping for different fire probabilities
    for i in range(0, 11, 1):
        fireprob = i / 10
        successCount = 0
        fairTrails = 0
        for _ in itertools.repeat(None, N):
            response = mazeWithFireRebuild(dim, fillProb, fireprob)  # Calling required method. Can be any of three
            # strategies
            print(response)
            if response is None:  # If no initial solution, discarding that maze
                continue
            for result in response:  # As list only contains legal maze iterations, finding whether dead or alive
                if result == 'alive':
                    successCount = successCount + 1
                    fairTrails = fairTrails + 1
                elif result == 'dead':
                    fairTrails = fairTrails + 1
        # Printing the output
        print('Fair trails are ' + str(fairTrails))
        print('Success Count is ' + str(successCount))
        print('Winning probability is ' + str(successCount / fairTrails))
        print(str(fireprob) + ',' + str(fairTrails) + ',' + str(successCount) + ',' + str(successCount / fairTrails))
        # Storing the output for each fire probability and printing all in the end in csv format
        storageDict[str(fireprob)] = str(fireprob) + ',' + str(fairTrails) + ',' + str(successCount) + ',' + str(
            successCount / fairTrails)
    for prob in storageDict.values():
        print(prob)


# Running driver code
test_strategies()
