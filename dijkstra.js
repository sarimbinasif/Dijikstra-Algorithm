const { performance } = require("perf_hooks");

// creating class for priority queue
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

// main dijkstra algorithm
function dijkstra(graph, start, end) {
  let distances = {};
  let previous = {};
  // priority queue to keep track of vertices to visit (initially start node is added)
  let pq = new PriorityQueue();

  // distances for all vertices is infinity in beginning except for the start node itself, which has distance of 0
  for (let vertex in graph) {
    if (vertex === start) {
      distances[vertex] = 0;
      pq.enqueue(vertex, 0);
    } else {
      distances[vertex] = Infinity;
      pq.enqueue(vertex, Infinity);
    }
    // for all vertices, previous node is set to None
    previous[vertex] = null;
  }

  // as long as priority queue is filled with at least one vertex
  while (!pq.isEmpty()) {
    let { element: currentNode } = pq.dequeue();

    // nothing to do if current distance is greater than previous distance
    if (currentNode === end) break;

    for (let neighbor in graph[currentNode]) {
      let alt = distances[currentNode] + graph[currentNode][neighbor];
      // if smaller distance is found
      if (alt < distances[neighbor]) {
        distances[neighbor] = alt;
        // set the previous node for this neighbor as current node
        previous[neighbor] = currentNode;
        // add neighbor to priority queue
        pq.enqueue(neighbor, alt);
      }
    }
  }

  // go back from the last vertex to previous vertex and then to its previous vertex, and so on to create path
  let path = [];
  let current = end;
  while (current) {
    path.unshift(current);
    current = previous[current];
  }

  // return shortest distance from start to end, and the path which is an array of vertices
  return { distance: distances[end], path };
}

// initializing a graph
const graph = {
  A: { B: 2, C: 4 },
  B: { A: 2, D: 7, E: 3 },
  C: { A: 4, F: 6 },
  D: { B: 7, E: 1, G: 3 },
  E: { B: 3, D: 1, H: 2 },
  F: { C: 6, I: 8 },
  G: { D: 3, J: 4 },
  H: { E: 2, I: 5 },
  I: { F: 8, H: 5, J: 1 },
  J: { G: 4, I: 1 },
};

console.log(""); // to give a line gap
// calculating execution time and peak memory usage
const start = performance.now();
const startMemory = process.memoryUsage().heapUsed; // initial memory usage
const { distance, path } = dijkstra(graph, "A", "J");
const endMemory = process.memoryUsage().heapUsed; // final memory usage
const end = performance.now();
const exec_time = end - start;

console.log("[NODE.JS]");

console.log("\nOutput:");
console.log(`Shortest distance from start to end: ${distance}`);
console.log(`Path: ${path}`);

console.log("\nAnalytics:");
console.log("Execution time: " + exec_time.toFixed(10) + " ms");
const peakMemory = (endMemory - startMemory) / 1024; // in KB
console.log(`Peak memory usage: ${peakMemory.toFixed(4)} KB\n`);
