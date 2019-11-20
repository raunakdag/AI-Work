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

# Change current working directory, only needed for Atom
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def calcd(y1, x1, y2, x2):

    if y1 == y2 and x1 == x2:
        return 0

    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    y1 = float(y1)
    x1 = float(x1)
    y2 = float(y2)
    x2 = float(x2)

    R = 3958.76  # miles = 6371 km

    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0

    # approximate great circle distance with law of cosines

    return acos(sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1)) * R


def read_files():
    start = time.perf_counter()

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
    # edge_cost = {}
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
        modlat = (lat - 10)/60  # scales to 0-1
        modlong = (long + 130)/70  # scales to 0-1
        map_locations[node] = [modlat*800, modlong*1200]
        # print(map_locations[node])

    end = time.perf_counter()

    print("Time to create data structure: " + str(end-start) + " seconds")

    return city_to_node, node_location, neighbors, map_locations  # , edge_cost


def a_star(start, goal, node_location, neighbors, ROOT2, canvas2, map_locations):

    closed = set()

    start_node = (a_star_heuristic(start, goal, node_location), start, [])
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
                    new_cost = current[0] - a_star_heuristic(current[1], goal, node_location) + a_star_heuristic(
                        current[1], neighboring_city, node_location) + a_star_heuristic(neighboring_city, goal, node_location)
                    current[2].append(neighboring_city)
                    heappush(heap, (new_cost, neighboring_city, current[2]))

                    y1, x1 = map_locations[str(current[1])]
                    y2, x2 = map_locations[str(neighboring_city)]
                    draw_line(canvas2, y1, x1, y2, x2, 'green')  # graph[5] is map dict
                    if counter % 100 == 0:
                        ROOT2.update()
                        counter = 1

    return None


def a_star_heuristic(start, end, node_location):
    y1, x1 = node_location[str(start)]
    y2, x2 = node_location[str(end)]
    return calcd(y1, x1, y2, x2)


def djikstra(start, goal, node_location, neighbors, ROOT, canvas, map_locations):
    closed = set()

    start_node = (0, start, a_star_heuristic(start, goal, node_location))
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
                    total_cost = current[2] - a_star_heuristic(current[1], goal, node_location) + a_star_heuristic(
                        current[1], neighboring_city, node_location) + a_star_heuristic(neighboring_city, goal, node_location)
                    new_cost = current[2] + \
                        a_star_heuristic(current[1], neighboring_city, node_location) - \
                        a_star_heuristic(current[1], goal, node_location)
                    heappush(heap, (new_cost, neighboring_city, total_cost))

                    y1, x1 = map_locations[str(current[1])]
                    y2, x2 = map_locations[str(neighboring_city)]
                    draw_line(canvas, y1, x1, y2, x2, 'green')  # graph[5] is map dict

                    if counter % 2000 == 0:
                        ROOT.update()
                        counter = 1

    return None


def draw_line(canvas, y1, x1, y2, x2, col):
    x1, y1, x2, y2 = float(x1), float(y1), float(x2), float(y2)
    # print(str(x1) + " " + str(y1))
    canvas.create_line(x1, 800-y1, x2, 800-y2, fill=col)


def draw_all_edges(ROOT, canvas, neighbors, map_locations):
    # print(node_location)
    ROOT.geometry("1200x800")  # sets geometry
    canvas.pack(fill=BOTH, expand=1)  # sets fill expand
    canvas.create_text(600, 80, fill="white", font="Times 36 bold",
                       text="The Map of the US :)")

    for neighbor in neighbors:
        for neighbor_of in neighbors[neighbor]:
            y1, x1 = map_locations[str(neighbor)]
            y2, x2 = map_locations[str(neighbor_of)]
            draw_line(canvas, y1, x1, y2, x2, 'white')

    ROOT.update()


def main():
    city_to_node, node_location, neighbors, map_locations = read_files()
    ROOT = Tk()  # creates new tkinter
    ROOT.title("Visualization Djikstra")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, neighbors, map_locations)

    # city_to_node, node_location, neighbors, edge_cost = read_files()

    city1, city2 = sys.argv[1], sys.argv[2]
    # city1 = 'Ciudad Juarez'
    # city2 = 'Montreal'

    start = time.perf_counter()
    cost = djikstra(city_to_node[city1], city_to_node[city2],
                    node_location, neighbors, ROOT, canvas, map_locations)
    end = time.perf_counter()

    print(city1 + " to " + city2 + " with Djikstra: " +
          str(cost) + " in " + str(end-start) + " seconds")
    time.sleep(15)
    ROOT.destroy()

    ROOT2 = Tk()
    ROOT2.title("Visualization A*")
    canvas2 = Canvas(ROOT2, background='black')  # sets background
    draw_all_edges(ROOT2, canvas2, neighbors, map_locations)

    start = time.perf_counter()
    cost = a_star(city_to_node[city1], city_to_node[city2],
                  node_location, neighbors, ROOT2, canvas2, map_locations)
    end = time.perf_counter()

    print(city1 + " to " + city2 + " with A*: " + str(cost) + " in " + str(end-start) + " seconds")
    time.sleep(15)
    ROOT.destroy()


main()
