__author__ = "Aravinda Reddy Dandu"

import copy
import itertools
from pprint import pprint
from random import randint
import numpy as np

import Fire_Maze
from Fire_Maze import Location

simulatonsPerMaze = 10


# Fake fire strategy. Using same variables as first and second strategies
def mazeWithFireThirdStrategy(dim, fillProb, fireprob):
    source = Location(0, 0)
    dest = Location(dim - 1, dim - 1)
    cleanMaze = Fire_Maze.generateGrid(dim, fillProb)
    initialsolution = Fire_Maze.getSolution(source, dest, cleanMaze)
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
            heat = 5  # Declaring a heat variable. This determines the number of iterations fake fire has to be
            # spread. Lessens for every iteration.
            solution = copy.deepcopy(initialsolution)
            firecell = Location(randint(0, dim - 1), randint(0, dim - 1))
            while visited[firecell.x][firecell.y] or (Fire_Maze.breadthFirstSearch(maze, Location(0, 0), firecell) == -1):
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
                maze = Fire_Maze.spreadFire(maze, fireprob, False)
                solution = 0
                if heat == 0:  # If heat is 0, making it 1 to have some degree of foresight
                    heat = 1
                while solution == 0 and heat > 0:  # Spreading fake fire. Heat is number of iterations and fire
                    # probability is 1. Iterating until a path is found.
                    maze = spreadFakeFire(maze, heat, 1)
                    solution = Fire_Maze.getSolution(point, dest, maze)
                    heat = heat - 1
                # heat = heat + 1
                maze = [[1 if b == 4 else b for b in i] for i in maze]  # Putting off the fake fire after finding
                # solution
                if solution == 0:  # If fake fire blocks all paths, finding solution with actual fire
                    solution = Fire_Maze.getSolution(point, dest, maze)
                    if solution == 0:  # Dead if no solution found
                        mazeCount.append('dead')
                        print('Point is ' + str(point.x) + ',' + str(point.y))
                        pprint(maze)
                        print('dead')
                        break
                point = solution[1]
                if point == dest:  # Alive if dest reached
                    pprint(maze)
                    mazeCount.append('alive')
                    print('alive')
                    break
                # elif maze[point.x][point.y] == 2:
                #     pprint(maze)
                #     mazeCount.append('dead')
                #     print('dead')
                #     break
        return mazeCount
        # pprint(maze)
        # return 'alive'


# Method to spread fake fire heat number of times
def spreadFakeFire(maze, heat, fireprob):
    maze = [[1 if b == 4 else b for b in i] for i in maze]
    if heat > 0:
        for _ in itertools.repeat(None, heat):
            maze = Fire_Maze.spreadFire(maze, fireprob, True)
    return maze


# Driver code to test strategy
def Run():
    global simulatonsPerMaze
    N = 10
    simulatonsPerMaze = 10
    storageDict = {}
    dim = 20
    fillprob = 0.7
    for i in [5]:
        fireprob = i / 10
        successCount = 0
        fairTrails = 0
        for _ in itertools.repeat(None, N):
            response = mazeWithFireThirdStrategy(dim=dim, fillProb=fillprob, fireprob=fireprob)
            print(response)
            if response is None:
                continue
            for result in response:
                if result == 'alive':
                    successCount = successCount + 1
                    fairTrails = fairTrails + 1
                elif result == 'dead':
                    fairTrails = fairTrails + 1
        print('Fair trails are ' + str(fairTrails))
        print('Success Count is ' + str(successCount))
        print('Winning probability is ' + str(successCount / fairTrails))
        print(str(fireprob) + ',' + str(fairTrails) + ',' + str(successCount) + ',' + str(successCount / fairTrails))
        storageDict[str(fireprob)] = str(fireprob) + ',' + str(fairTrails) + ',' + str(successCount) + ',' + str(
            successCount / fairTrails)
    for prob in storageDict.values():
        print(prob)


Run()
