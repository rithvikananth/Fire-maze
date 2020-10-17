import numpy as np
import random
from pprint import pprint

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

def generateGrid(dim, prob):
    # dim = 10
    grid = []
    for row in range(dim):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(dim):
            grid[row].append(int(np.random.binomial(1, 1- prob, 1)))  # Append a cell
            if row == column == dim - 1:
                grid[row][column] = 0
    grid[0][0] = 0
    grid[dim - 1][dim - 1] = 0
    return grid


def astar(maze, heuristic, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        if heuristic == "All_direction":
            adj_nodes = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        else :
            adj_nodes = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for new_position in adj_nodes: # Adjacent squares
            # add (-1, -1), (-1, 1), (1, -1), (1, 1) in the above list for travelling diagonally in the maze.
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure the children are within the maze boundaries
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # skip if the child node is a blockage i.e. 1
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # if the child node is already in closed list then we ignore it
            if new_node in closed_list:
                continue

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # square of euclidian distance as heuristics
            if heuristic == "Euclidian":
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            # Manhattan distance heuristic
            else:
                child.h = (abs(end_node.position[0] - child.position[0]) + abs(end_node.position[1] - child.position[1]))
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            if child not in open_list:
                open_list.append(child)
        #print(len(open_list))

def mazepath(maze_path, path):
    w = len(maze_path)
    for row in range(w):
        for column in range(w):
            if (row, column) in path:
                maze_path[row][column] = 0
            else:
                maze_path[row][column] = 1
    return maze_path


def thinmaze(maze,prob):
    w = len(maze)
    l1 = []
    l2 = []
    c = []
    for row in range(w):
        for column in range(w):
            if maze[row][column] == 1:
                c = (row, column)
                l1.append(c)
    count = int(round((len(l1))*prob))
    print(count)
    for i in range(0, count):
        a = random.choice(l1)
        l2.append(a)
        l1.remove(a)
        i += 1
    for row in range(w):
        for column in range(w):
            if (row, column) in l2:
                maze[row][column] = 0
    return maze

def thin_heuristic(thin_maze, start_node, end_node):
    dist = "Manhattan"
    thinPath = astar(thin_maze, dist, start_node, end_node)
    return len(thinPath) if thinPath != None else 0

def astar_thinning(maze,thin_maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            # add (-1, -1), (-1, 1), (1, -1), (1, 1) in the above list for travelling diagonally in the maze.
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure the children are within the maze boundaries
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # skip if the child node is a blockage i.e. 1
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # if the child node is already in closed list then we ignore it
            if new_node in closed_list:
                continue

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # square of euclidian distance as heuristics
            #child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            # Manhattan distance heuristic
            child.h = thin_heuristic(thin_maze, child.position, end_node.position)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            if child not in open_list:
                open_list.append(child)
        #print(len(open_list))

def main():
    trails = 5
    rho = 0.15     # removing (rho*100) % of the obstacles from the maze
    success = 0
    success_thin = 0
    success_all = 0
    for i in range(1, trails + 1):
        maze = generateGrid(10, 0.7)
        #0 is free path and 1 is blocked path
        start = (0, 0)
        end = (9, 9)
        heuristic = "Manhattan"
        path = astar(maze, heuristic, start, end)
        print("Trail No:", i)
        if path == None:
            print('No path from source to the goal')
        else:
            print("There is a path from source to goal")
            success += 1
            maze1 = mazepath(maze, path)
            pprint(maze1)
        print("After maze thinning")
        #removing a fraction of obstacles in the maze
        thin_maze = thinmaze(maze, rho)
        thin_path = astar_thinning(maze, thin_maze, start, end)
        if thin_path == None:
            print('No path from source to the goal')
        else:
            print("There is a path from source to goal")
            success_thin += 1
            maze2 = mazepath(maze, thin_path)
            pprint(maze2)
        heuristic = "All_direction"
        All_directions_path = astar(maze, heuristic, start, end)
        if All_directions_path == None:
            print('No path from source to the goal')
        else:
            print("There is a path from source to goal")
            success_all += 1
            maze3 = mazepath(maze, All_directions_path)
        i += 1
    success_prob = (success / trails) * 100
    print("Success % with A Star manhattan distance is", success_prob, "%")
    success_prob_thin = (success_thin / trails) * 100
    print("Success % with A Star thinning with rho value ", rho * 100, "% of the obstacles is",success_prob_thin, "%")
    success_prob_all = (success_all / trails) * 100
    print("Success % with A Star with movement restriction relaxation direction moment is", success_prob_all, "%")


if __name__ == '__main__':
    thin_path = []
    main()









