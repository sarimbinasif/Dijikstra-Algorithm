import heapq
import networkx as nx
import matplotlib.pyplot as plt
import time
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
                # add neighbor to priority queue only if distance is updated
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
graph10 = {
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

graph25 = {
    'A': [('B', 2), ('C', 4)],
    'B': [('D', 7), ('E', 3), ('X', 3)],
    'C': [('F', 6)],
    'D': [('E', 1), ('G', 3)],
    'E': [('D', 1), ('H', 2)],
    'F': [('I', 8)],
    'G': [('J', 4), ('W', 6)],
    'H': [('I', 5)],
    'I': [('F', 8), ('H', 5), ('J', 1)],
    'J': [('G', 4), ('I', 1), ('K', 2)],
    'K': [('L', 2), ('M', 4)],
    'L': [('N', 7), ('O', 3)],
    'M': [('P', 6)],
    'N': [('O', 1), ('Q', 3)],
    'O': [('N', 1), ('R', 2)],
    'P': [('S', 8)],
    'Q': [('T', 4)],
    'R': [('S', 5)],
    'S': [('P', 8), ('R', 5), ('T', 1)],
    'T': [('Q', 4), ('S', 1), ('U', 3)],
    'U': [('V', 2), ('W', 4)],
    'V': [('X', 7), ('Y', 3)],
    'W': [('G', 6)],
    'X': [('V', 7), ('Y', 1)],
    'Y': [('V', 3), ('D', 2)],
}

graph50 = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('A', 1), ('E', 2), ('F', 4)],
    'C': [('A', 3), ('F', 1), ('G', 4)],
    'D': [('A', 7), ('G', 2), ('H', 5)],
    'E': [('B', 2), ('H', 5), ('I', 3)],
    'F': [('B', 4), ('C', 1), ('I', 3)],
    'G': [('C', 4), ('D', 2), ('J', 6)],
    'H': [('D', 5), ('E', 5), ('K', 4)],
    'I': [('E', 3), ('F', 3), ('L', 2), ('M', 3)],
    'J': [('G', 6), ('N', 5), ('K', 3)],
    'K': [('H', 4), ('J', 3), ('O', 7)],
    'L': [('I', 2), ('P', 4), ('M', 3)],
    'M': [('I', 3), ('L', 3), ('Q', 6)],
    'N': [('J', 5), ('R', 4), ('O', 6)],
    'O': [('K', 7), ('N', 6), ('S', 2)],
    'P': [('L', 4), ('T', 3), ('Q', 5)],
    'Q': [('M', 6), ('P', 5), ('U', 5)],
    'R': [('N', 4), ('V', 3), ('S', 7)],
    'S': [('O', 2), ('R', 7), ('W', 4)],
    'T': [('P', 3), ('X', 6), ('U', 5)],
    'U': [('Q', 5), ('T', 5), ('Y', 4)],
    'V': [('R', 3), ('Z', 7), ('W', 6)],
    'W': [('S', 4), ('V', 6), ('AA', 5)],
    'X': [('T', 6), ('AB', 2), ('Y', 4)],
    'Y': [('U', 4), ('X', 4), ('AC', 3), ('BB', 5)],
    'Z': [('V', 7), ('AD', 6), ('AA', 5)],
    'AA': [('W', 5), ('Z', 5), ('AE', 4)],
    'AB': [('X', 2), ('AF', 7), ('AC', 5)],
    'AC': [('Y', 3), ('AB', 5), ('AG', 6)],
    'AD': [('Z', 6), ('AH', 5), ('AE', 7)],
    'AE': [('AA', 4), ('AD', 7), ('AI', 3)],
    'AF': [('AB', 7), ('AJ', 2), ('AG', 5)],
    'AG': [('AC', 6), ('AF', 5), ('AK', 4)],
    'AH': [('AD', 5), ('AL', 6), ('AI', 4)],
    'AI': [('AE', 3), ('AH', 4), ('AM', 2)],
    'AJ': [('AF', 2), ('AN', 5), ('AK', 4)],
    'AK': [('AG', 4), ('AJ', 4), ('AO', 3)],
    'AL': [('AH', 6), ('AP', 7), ('AM', 5)],
    'AM': [('AI', 2), ('AL', 5), ('AQ', 5)],
    'AN': [('AJ', 5), ('AR', 4), ('AO', 3)],
    'AO': [('AK', 3), ('AN', 3), ('AS', 6)],
    'AP': [('AL', 7), ('AT', 4), ('AQ', 5)],
    'AQ': [('AM', 5), ('AP', 5), ('AU', 3)],
    'AR': [('AN', 4), ('AV', 2), ('AS', 4)],
    'AS': [('AO', 6), ('AR', 4), ('AW', 5)],
    'AT': [('AP', 4), ('AX', 3), ('AU', 5)],
    'AU': [('AQ', 3), ('AT', 5), ('AY', 6)],
    'AV': [('AR', 2), ('AZ', 4), ('AW', 3)],
    'AW': [('AS', 5), ('AV', 3), ('BA', 3)],
    'AX': [('AT', 3), ('BB', 7), ('AY', 4)],
    'AY': [('AU', 6), ('AX', 4), ('BC', 5)],
    'AZ': [('AV', 4), ('BD', 3), ('BA', 6)],
    'BA': [('AW', 3), ('AZ', 6), ('BE', 6)],
    'BB': [('AX', 7), ('BF', 5), ('BC', 4), ('Y', 5)],
    'BC': [('AY', 5), ('BB', 4), ('BG', 4)],
    'BD': [('AZ', 3), ('BH', 6), ('BE', 5), ('BF', 7)],
    'BE': [('BA', 6), ('BD', 5), ('BI', 3)],
    'BF': [('BB', 5), ('BJ', 7), ('BG', 2), ('BD', 7)],
    'BG': [('BC', 4), ('BF', 2), ('BK', 2)],
    'BH': [('BD', 6), ('BL', 4), ('BI', 5)],
    'BI': [('BE', 3), ('BH', 5), ('BM', 5)],
    'BJ': [('BF', 7), ('BN', 6), ('BK', 4)],
    'BK': [('BG', 2), ('BJ', 4), ('BO', 4)],
    'BL': [('BH', 4), ('BM', 6)],
    'BM': [('BI', 5), ('BL', 6)],
    'BN': [('BJ', 6), ('BO', 5)],
    'BO': [('BK', 4), ('BN', 5)]
}

def test_case(test_case_name, graph, start, end):
    # finding execution time and peak memory usage
    tracemalloc.start()
    start_time = time.perf_counter()
    distance, path = dijkstra(graph, start, end)
    peak_memory = tracemalloc.get_traced_memory()[1]
    end_time = time.perf_counter()
    tracemalloc.stop()

    # Output
    print(f"\nPYTHON TEST CASE: {test_case_name}")
    print("\nOutput:")
    print(f"Shortest distance from {start} to {end}: {distance}")
    print(f"Path: {' -> '.join(path)}")
    print("\nAnalytics:")
    print(f"Peak memory usage: {peak_memory / 1024:.4f} KB")
    print(f"Execution time: {(end_time - start_time) * 1000:.10f} milliseconds\n")
    print("------------------------------------")

    # for visualization
    G = nx.Graph()
    for node, edges in graph.items():
        for neighbor, weight in edges:
            # adding each edge to graph
            G.add_edge(node, neighbor, weight=weight)

    # drawing vertices
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=200, font_size=10)

    # highlighting the shortest path in red
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="red", width=2)

    # adding edge weights as labels
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    # showing the graph
    plt.title("Dijkstra's Algorithm Visualization")
    plt.show()
    
test_case("10 Vertices", graph10, 'A', 'J')
test_case("25 Vertices", graph25, 'A', 'Q')
test_case("50 Vertices", graph50, 'A', 'BM')
