import heapq
import networkx as nx
import matplotlib.pyplot as plt
import time
import os
import tracemalloc

# main dijkstra algorithm
def dijkstra(graph, start, end):
    # distances for all vertices is infinity in beginning except for the start node itself, which has distance of 0
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    # priority queue to keep track of vertices to visit (initially start node is added)
    priority_queue = [(0, start)] # left = distance, right = vertex
    # for all vertices, previous node is set to None
    previous_nodes = {node: None for node in graph}

    while priority_queue: # as long as priority queue is filled with at least one vertex
        current_distance, current_node = heapq.heappop(priority_queue)
        # if end is reached
        if current_node == end:
            break
        
        # nothing to do if current distance is greater than previous distance
        if current_distance > distances[current_node]:
            continue

        
        for neighbor, weight in graph[current_node]:
            # print(neighbor, weight)
            distance = current_distance + weight
            # if smaller distance is found
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                # set the previous node for this neighbor as current node
                previous_nodes[neighbor] = current_node
                # add neighbor to priority queue
                heapq.heappush(priority_queue, (distance, neighbor))

    # go back from the last vertex to previous vertex and then to its previous vertex, and so on to create path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()
    # return shortest distance from start to end, and the path which is an array of vertices
    return distances[end], path

# initializing a graph
graph = {
    'A': [('B', 2), ('C', 4)],
    'B': [('A', 2), ('D', 7), ('E', 3)],
    'C': [('A', 4), ('F', 6)],
    'D': [('B', 7), ('E', 1), ('G', 3)],
    'E': [('B', 3), ('D', 1), ('H', 2)],
    'F': [('C', 6), ('I', 8)],
    'G': [('D', 3), ('J', 4)],
    'H': [('E', 2), ('I', 5)],
    'I': [('F', 8), ('H', 5), ('J', 1)],
    'J': [('G', 4), ('I', 1)],
}

# finding execution time and peak memory usage
tracemalloc.start()
start_time = time.perf_counter()
distance, path = dijkstra(graph, 'A', 'J')
peak_memory = tracemalloc.get_traced_memory()[1]
end_time = time.perf_counter()
tracemalloc.stop()

# Output
print("\n[PYTHON]")
print("\nOutput:")
print(f"Shortest distance from start to end: {distance}")
print(f"Path: {' -> '.join(path)}")
print("\nAnalytics:")
print(f"Peak memory usage: {peak_memory / 1024:.4f} KB")
print(f"Execution time: {(end_time - start_time) * 1000:.10f} milliseconds\n")

# for visualization
G = nx.Graph()
for node, edges in graph.items():
    for neighbor, weight in edges:
        # adding each edge to graph
        G.add_edge(node, neighbor, weight=weight)

# drawing vertices
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10)

# highlighting the shortest path in red
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)

# adding edge weights as labels
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# showing the graph
plt.title("Dijkstra's Algorithm Visualization")
plt.show()
