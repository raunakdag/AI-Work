# Raunak Daga
# Mr. Eckel 5th PD AI
# Train Routes Part 1

from math import pi, acos, sin, cos
import os
import sys
import time
import heapq
from heapq import heappush, heappop
from tkinter import *
import time

cities = [
    "Albuquerque",
    "Atlanta",
    "Austin",
    "Brooklyn",
    "Calgary",
    "Charlotte",
    "Chicago",
    "Chihuahua",
    "Ciudad Juarez",
    "Columbus",
    "Dallas",
    "Denver",
    "Detroit",
    "Edmonton",
    "Fort Worth",
    "Guadalajara",
    "Hermosillo",
    "Houston",
    "Indianapolis",
    "Jacksonville",
    "Kansas City",
    "Las Vegas",
    "Leon",
    "Los Angeles",
    "Merida",
    "Mexicali",
    "Mexico City",
    "Miami",
    "Milwaukee",
    "Minneapolis",
    "Monterrey",
    "Montreal",
    "Orlando",
    "Ottawa",
    "Philadelphia",
    "Phoenix",
    "Portland",
    "Quebec City",
    "St Louis",
    "San Antonio",
    "San Diego",
    "San Francisco",
    "San Jose",
    "Seattle",
    "Tampa",
    "Toronto",
    "Tucson",
    "Vancouver",
    "Washington DC",
    "Winnipeg"
]

algorithms = [
    "A-Star",
    "Djikstra",
    "DFS",
    "ID-DFS"
]

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def calcd(y1, x1, y2, x2):
    if y1 == y2 and x1 == x2:
        return 0
    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)
    R = 3958.76  # miles = 6371 km
    y1 *= pi / 180.0
    x1 *= pi / 180.0
    y2 *= pi / 180.0
    x2 *= pi / 180.0
    return acos(sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x2 - x1)) * R


def read_files():
    city_to_node = {}
    with open('rrNodeCity.txt') as city_list:
        for line in city_list:
            city_to_node[str(line[8:]).replace('\n', '')] = str(line[0:7])

    node_location = {}
    with open('rrNodes.txt') as nodes_list:
        for line in nodes_list:
            node, y, x = line.strip().split(" ")
            node_location[node] = (y, x)  # Flip Latitude and Longitude

    neighbors = {}
    with open('rrEdges.txt') as neighbors_list:
        for line in neighbors_list:
            n1, n2 = line.strip().split(" ")
            if n1 in neighbors:
                neighbors[n1].append(n2)
            else:
                neighbors[n1] = [n2]

            if n2 in neighbors:
                neighbors[n2].append(n1)
            else:
                neighbors[n2] = [n1]

    map_locations = {}
    for node in node_location:
        y, x = node_location[node]
        lat = float(y)  # gets latitude
        long = float(x)  # gets long
        modlat = (lat - 10) / 60  # scales to 0-1
        modlong = (long + 130) / 70  # scales to 0-1
        map_locations[node] = [modlat * 800, modlong * 1200]

    return city_to_node, node_location, neighbors, map_locations


def a_star(start, goal, node_location, neighbors, ROOT2, canvas2, map_locations, speed_slider):
    closed = set()

    start_node = (heuristic(start, goal, node_location), start, [])
    heap = []
    heappush(heap, start_node)

    counter = 0
    while heap:
        current = heappop(heap)
        counter += 1
        if current[1] == goal:
            ROOT2.update()
            return current[0]

        if current[1] not in closed:
            closed.add(current[1])
            for neighboring_city in neighbors[current[1]]:
                if neighboring_city not in closed:
                    new_cost = current[0] - heuristic(current[1], goal, node_location) + heuristic(
                        current[1], neighboring_city, node_location) + heuristic(neighboring_city, goal, node_location)
                    current[2].append(neighboring_city)
                    heappush(heap, (new_cost, neighboring_city, current[2]))

                    y1, x1 = map_locations[str(current[1])]
                    y2, x2 = map_locations[str(neighboring_city)]
                    draw_line(canvas2, y1, x1, y2, x2, 'green')
                    if counter % speed_slider == 0:
                        ROOT2.update()
                        counter = 1

    return None


def djikstra(start, goal, node_location, neighbors, ROOT, canvas, map_locations, speed_slider):
    closed = set()

    start_node = (0, start, heuristic(start, goal, node_location))
    heap = []
    heappush(heap, start_node)

    counter = 0
    while heap:
        current = heappop(heap)
        counter += 1
        if current[1] == goal:
            ROOT.update()
            return current[2]

        if current[1] not in closed:
            closed.add(current[1])
            for neighboring_city in neighbors[current[1]]:
                if neighboring_city not in closed:
                    total_cost = current[2] - heuristic(current[1], goal, node_location) + heuristic(
                        current[1], neighboring_city, node_location) + heuristic(neighboring_city, goal, node_location)
                    new_cost = current[2] + \
                        heuristic(current[1], neighboring_city, node_location) - \
                        heuristic(current[1], goal, node_location)
                    heappush(heap, (new_cost, neighboring_city, total_cost))

                    y1, x1 = map_locations[str(current[1])]
                    y2, x2 = map_locations[str(neighboring_city)]
                    # graph[5] is map dict
                    draw_line(canvas, y1, x1, y2, x2, 'green')

                    if counter % speed_slider == 0:
                        ROOT.update()
                        counter = 1

    return None


def dfs(start, goal, node_location, neighbors, ROOT, canvas, map_locations, speed_slider):
    fringe = []
    closed = set()

    start_node = (start, heuristic(start, goal, node_location))

    fringe.append(start_node)

    counter = 0
    while(fringe):
        current = fringe.pop(0)
        counter += 1

        if(current[0] == goal):
            return current[1]

        if current[0] not in closed:
            closed.add(current[0])
            for neighboring_city in neighbors[current[0]]:
                if neighboring_city not in closed:
                    new_cost = current[1] - heuristic(current[0], goal, node_location) + heuristic(
                        current[0], neighboring_city, node_location) + heuristic(neighboring_city, goal, node_location)

                    new_node = (neighboring_city, new_cost)
                    fringe.append(new_node)

                    y1, x1 = map_locations[str(current[0])]
                    y2, x2 = map_locations[str(neighboring_city)]
                    draw_line(canvas, y1, x1, y2, x2, 'green')
                    if counter % speed_slider == 0:
                        ROOT.update()
                        counter = 0

    return None


def kDFS(start, goal, node_location, neighbors, ROOT, canvas, map_locations, k, speed_slider):
    start_node = (start, heuristic(start, goal, node_location), 0)
    fringe = [start_node]
    closed = set()

    counter = 0
    while(fringe):
        current = fringe.pop()
        counter += 1

        if(current[0] == goal):
            return current[1]

        if current[2] < k:
            if current[0] not in closed:
                closed.add(current[0])
                for neighboring_city in neighbors[current[0]]:
                    if neighboring_city not in closed:
                        new_cost = current[1] - heuristic(current[0], goal, node_location) + heuristic(
                            current[0], neighboring_city, node_location) + heuristic(neighboring_city, goal, node_location)
                        new_node = (neighboring_city, new_cost, current[2] + 1)
                        fringe.append(new_node)

                        y1, x1 = map_locations[str(current[0])]
                        y2, x2 = map_locations[str(neighboring_city)]
                        draw_line(canvas, y1, x1, y2, x2, 'green')
                        if counter % speed_slider == 0:
                            ROOT.update()
                            counter = 0

    return None


def id_dfs(start, goal, node_location, neighbors, ROOT, canvas, map_locations, speed_slider):
    cost = None
    k = 0
    while cost is None:
        cost = kDFS(start, goal, node_location, neighbors, ROOT,
                    canvas, map_locations, k, speed_slider)
        k += 1
    return cost


def heuristic(start, end, node_location):
    y1, x1 = node_location[str(start)]
    y2, x2 = node_location[str(end)]
    return calcd(y1, x1, y2, x2)


def draw_line(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    canvas.create_line(x1, 650 - y1, x2, 650 - y2, fill=col)


def draw_all_edges(ROOT, canvas, neighbors, map_locations):
    for neighbor in neighbors:
        for neighbor_of in neighbors[neighbor]:
            y1, x1 = map_locations[str(neighbor)]
            y2, x2 = map_locations[str(neighbor_of)]
            draw_line(canvas, y1, x1, y2, x2, 'white')

    ROOT.update()


def main_visualization():
    ROOT.update_idletasks()

    city1_name = city1.get()
    city2_name = city2.get()
    algorithm_name = algorithm.get()
    speed_slider = scale.get()

    if 'A-' in algorithm_name:
        start = time.perf_counter()
        cost = a_star(city_to_node[city1_name], city_to_node[city2_name],
                      node_location, neighbors, ROOT, canvas, map_locations, speed_slider)
        end = time.perf_counter()
        print(city1_name + " to " + city2_name + " with A*: " +
              str(cost) + " in " + str(end - start) + " seconds")
    elif 'Dji' in algorithm_name:
        start = time.perf_counter()
        cost = djikstra(city_to_node[city1_name], city_to_node[city2_name],
                        node_location, neighbors, ROOT, canvas, map_locations, speed_slider)
        end = time.perf_counter()
        print(city1_name + " to " + city2_name + " with Djikstra: " +
              str(cost) + " in " + str(end - start) + " seconds")
    elif algorithm_name == 'DFS':
        start = time.perf_counter()
        cost = dfs(city_to_node[city1_name], city_to_node[city2_name],
                   node_location, neighbors, ROOT, canvas, map_locations, speed_slider)
        end = time.perf_counter()
        print(city1_name + " to " + city2_name + " with DFS: " +
              str(cost) + " in " + str(end - start) + " seconds")
    elif algorithm_name == 'ID-DFS':
        start = time.perf_counter()
        cost = id_dfs(city_to_node[city1_name], city_to_node[city2_name],
                      node_location, neighbors, ROOT, canvas, map_locations, speed_slider)
        end = time.perf_counter()
        print(city1_name + " to " + city2_name + " with ID-DFS: " +
              str(cost) + " in " + str(end - start) + " seconds")


def reset():
    ROOT.update_idletasks()
    canvas.delete('all')
    draw_all_edges(ROOT, canvas, neighbors, map_locations)
    ROOT.update()


city_to_node, node_location, neighbors, map_locations = read_files()

ROOT = Tk()
ROOT.title("Visualization Djikstra")
ROOT.geometry("1200x800")
canvas = Canvas(ROOT, background='black', width=1200, height=600)
canvas.place(x=0, y=0)

city1 = StringVar(ROOT)
city1.set(cities[0])

city2 = StringVar(ROOT)
city2.set(cities[0])

algorithm = StringVar(ROOT)
algorithm.set(algorithms[0])

x = OptionMenu(ROOT, city1, *cities)
y = OptionMenu(ROOT, city2, *cities)
z = OptionMenu(ROOT, algorithm, *algorithms)

mapReset = Button(ROOT, text='Reset', command=reset)
doProcess = Button(ROOT, text="Visualize", command=main_visualization)

scale = Scale(ROOT, label='Speed', orient=HORIZONTAL, length=100, width=20,
              sliderlength=10, from_=0, to=1000, tickinterval=100)

x.place(x=0, y=600)
y.place(x=100, y=600)
z.place(x=200, y=600)
scale.place(x=300, y=600)
mapReset.place(x=500, y=600)
doProcess.place(x=600, y=600)

# map = PhotoImage(file='map.png')
# canvas.create_image(0, 0, image=map, anchor=NW)
draw_all_edges(ROOT, canvas, neighbors, map_locations)

ROOT.update()

ROOT.mainloop()
