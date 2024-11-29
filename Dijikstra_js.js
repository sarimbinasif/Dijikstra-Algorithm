const {performance} = require('perf_hooks');

class PriorityQueue {
    constructor() {
        this.queue = [];
    }

    enqueue(element, priority) {
        this.queue.push({ element, priority });
        this.sort();
    }

    dequeue() {
        return this.queue.shift();
    }

    isEmpty() {
        return this.queue.length === 0;
    }

    sort() {
        this.queue.sort((a, b) => a.priority - b.priority);
    }
}

function dijkstra(graph, start, end) {
    // Initialize distances, previous, and priority queue
    let distances = {};
    let previous = {};
    let pq = new PriorityQueue();

    for (let vertex in graph) {
        if (vertex === start) {
            distances[vertex] = 0;
            pq.enqueue(vertex, 0);
        } else {
            distances[vertex] = Infinity;
            pq.enqueue(vertex, Infinity);
        }
        previous[vertex] = null;
    }

    // Processing the priority queue
    while (!pq.isEmpty()) {
        let { element: currentNode } = pq.dequeue();

        // Stop if we reach the target node
        if (currentNode === end) break;

        for (let neighbor in graph[currentNode]) {
            let alt = distances[currentNode] + graph[currentNode][neighbor];

            // Update distances and enqueue if a shorter path is found
            if (alt < distances[neighbor]) {
                distances[neighbor] = alt;
                previous[neighbor] = currentNode;
                pq.enqueue(neighbor, alt);
            }
        }
    }

    // Reconstruct the shortest path
    let path = [];
    let current = end;
    while (current) {
        path.unshift(current);
        current = previous[current];
    }

    return { distance: distances[end], path };
}

// Example Graph
const graph = {
    'A': { 'B': 2, 'C': 4 },
    'B': { 'A': 2, 'D': 7, 'E': 3 },
    'C': { 'A': 4, 'F': 6 },
    'D': { 'B': 7, 'E': 1, 'G': 3 },
    'E': { 'B': 3, 'D': 1, 'H': 2 },
    'F': { 'C': 6, 'I': 8 },
    'G': { 'D': 3, 'J': 4 },
    'H': { 'E': 2, 'I': 5 },
    'I': { 'F': 8, 'H': 5, 'J': 1 },
    'J': { 'G': 4, 'I': 1 }
};

// Measure runtime + memory usage
//console.time("Dijkstra Runtime");
const startTime = performance.now();
const result = dijkstra(graph, 'A', 'J');
const endTime = performance.now();
const runtime = endTime - startTime;

//console.timeEnd("Dijkstra Runtime");

// Output the result
// console.log(`Shortest distance from A to J: ${result.distance}`);
console.log(`Runtime: ${runtime} ms`);

console.log(`Path: ${result.path.join(' -> ')}`);
