import heapq
import networkx as nx
import matplotlib.pyplot as plt
import time
import psutil
import os
import tracemalloc


# Function to get current memory usage
def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss  # Return memory usage in KB

# Dijkstra's Algorithm Implementation
def dijkstra(graph, start, end):
    # Measure memory usage before running Dijkstra
    memory_before = get_memory_usage()

    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            # print(neighbor, weight)
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Reconstruct the path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    
    # Measure memory usage after running Dijkstra
    memory_after = get_memory_usage()
    print(f"Memory Usage: Before: {memory_before:.10f} KB, After: {memory_after:.10f} KB")

    return distances[end], path





# Graph with 10 vertices
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
    'J': [('G', 4), ('I', 1)]
}




# Measure runtime
start_time = time.time()
# tracemalloc.start()
distance, path = dijkstra(graph, 'A', 'J')
# print(tracemalloc.get_traced_memory())
# tracemalloc.stop()
end_time = time.time()



run_time = end_time - start_time
run_time = run_time * 1000

# Output
print(f"Shortest distance: {distance}")
print(f"Path: {' -> '.join(path)}")
print(f"Runtime: {run_time: .6f} ms")


# Visualization
G = nx.Graph()
for node, edges in graph.items():
    for neighbor, weight in edges:
        G.add_edge(node, neighbor, weight=weight)

# Node positions and visualization
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=700, font_size=10)

# Highlight the shortest path in red
path_edges = list(zip(path, path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)

# Add edge weights as labels
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

# Show the plot
plt.title("Dijkstra's Algorithm Visualization")
plt.show()
