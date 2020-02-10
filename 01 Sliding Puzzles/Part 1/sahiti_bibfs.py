def bi_bfs(start, goal, graph, col):

    # Your code goes here

    ROOT = Tk()  # creates new tkinter
    ROOT.title("Bi-BFS")
    canvas = Canvas(ROOT, background='black')  # sets background
    draw_all_edges(ROOT, canvas, graph)

    counter = 0
    for_frontier, for_explored = deque(), {start: "s"}
    for_frontier.append(start)

    back_frontier, back_explored = deque(), {goal: "s"}
    back_frontier.append(goal)

    while for_frontier and back_frontier:
        for_node = for_frontier.popleft()
        back_node = back_frontier.popleft()

        if for_node in back_explored:
            path_for, cost_for = generate_path(for_node, for_explored, graph)
            path_back, cost_back = generate_path(for_node, back_explored, graph)
            path = path_for[:-1] + path_back[::-1]
            cost = cost_for + cost_back
            draw_final_path(ROOT, canvas, path, graph)

            return (path, cost, len(for_explored)+len(back_explored))

        if back_node in for_explored:
            path_for, cost_for = generate_path(back_node, for_explored, graph)
            path_back, cost_back = generate_path(back_node, back_explored, graph)
            path = path_for[:-2] + path_back[::-1]
            draw_final_path(ROOT, canvas, path, graph)
            cost = cost_for + cost_back
            return (path, cost, len(for_explored)+len(back_explored))

        for a in graph[3][for_node]:  # graph[3] is neighbors
            if a not in for_explored:
                for_explored[a] = for_node
                for_frontier.append(a)
                drawLine(canvas, *graph[5][for_node], *graph[5][a], col)

        for z in graph[3][back_node]:  # graph[3] is neighbors
            if z not in back_explored:
                back_explored[z] = back_node
                back_frontier.append(z)
                drawLine(canvas, *graph[5][back_node], *graph[5][z], col)

        counter += 1
        if counter % 100 == 0:
            ROOT.update()
    return None
