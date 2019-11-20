# Name:        Data:
import heapq
import random
import pickle
import math
import time
from math import pi, acos, sin, cos
from tkinter import *
from collections import deque


# NodeLocations, NodeToCity, CityToNode, Neighbors, EdgeCost
# Node: (lat, long) or (y, x), node: city, city: node, node: neighbors, (n1, n2): cost
def make_graph(nodes="rrNodes.txt", node_city="rrNodeCity.txt", edges="rrEdges.txt"):
    nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost = {}, {}, {}, {}, {}
    map = {}   # have screen coordinate for each node location

    # Your code goes here

    ''' Un-comment after you fill the nodeLoc dictionary.
   for node in nodeLoc: #checks each
      lat = float(nodeLoc[node][0]) #gets latitude
      long = float(nodeLoc[node][1]) #gets long
      modlat = (lat - 10)/60 #scales to 0-1
      modlong = (long+130)/70 #scales to 0-1
      map[node] = [modlat*800, modlong*1200] #scales to fit 800 1200
   '''
    return [nodeLoc, nodeToCity, cityToNode, neighbors, edgeCost, map]

# Retuen the direct distance from node1 to node2
# Use calc_edge_cost function.


def dist_heuristic(n1, n2, graph):

    # Your code goes here

    pass

# Create a city path.
# Visit each node in the path. If the node has the city name, add the city name to the path.
# Example: ['Charlotte', 'Hermosillo', 'Mexicali', 'Los Angeles']


def display_path(path, graph):

    # Your code goes here

    pass

# Using the explored, make a path by climbing up to "s"
# This method may be used in your BFS and Bi-BFS algorithms.


def generate_path(state, explored, graph):
    path = [state]
    cost = 0

    # Your code goes here

    return path[::-1], cost


def drawLine(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    canvas.create_line(x1, 800-y1, x2, 800-y2, fill=col)

# Draw the final shortest path.
# Use drawLine function.


def draw_final_path(ROOT, canvas, path, graph, col='red'):

    # Your code goes here

    ROOT.update()
    pass


def draw_all_edges(ROOT, canvas, graph):
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    for n1, n2 in graph[4]:  # graph[4] keys are edge set
        drawLine(canvas, *graph[5][n1], *graph[5][n2], 'white')  # graph[5] is map dict
    ROOT.update()


def bfs(start, goal, graph, col):
    ROOT = Tk()  # creates new tkinter
    ROOT.title("BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)

    counter = 0
    frontier, explored = deque(), {start: "s"}
    frontier.append(start)
    while frontier:
        s = frontier.popleft()
        if s == goal:
            path, cost = generate_path(s, explored, graph)
            draw_final_path(ROOT, canvas, path, graph)
            return path, cost
        for a in graph[3][s]:  # graph[3] is neighbors
            if a not in explored:
                explored[a] = s
                frontier.append(a)
                drawLine(canvas, *graph[5][s], *graph[5][a], col)
        counter += 1
        if counter % 100 == 0:
            ROOT.update()
    return None


def main():
    start, goal, third = input("Start city: "), input(
        "Goal city: "), input("Third city for tri-directional: ")
    graph = make_graph("rrNodes.txt", "rrNodeCity.txt", "rrEdges.txt")  # Task 1

    mainloop()  # Let TK windows stay still
