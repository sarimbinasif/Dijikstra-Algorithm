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
const graph10 = {
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

const graph25 = {
  A: { B: 2, C: 4 },
  B: { D: 7, E: 3, X: 3 },
  C: { F: 6 },
  D: { E: 1, G: 3 },
  E: { D: 1, H: 2 },
  F: { I: 8 },
  G: { J: 4, W: 6 },
  H: { I: 5 },
  I: { F: 8, H: 5, J: 1 },
  J: { G: 4, I: 1, K: 2 },
  K: { L: 2, M: 4 },
  L: { N: 7, O: 3 },
  M: { P: 6 },
  N: { O: 1, Q: 3 },
  O: { N: 1, R: 2 },
  P: { S: 8 },
  Q: { T: 4 },
  R: { S: 5 },
  S: { P: 8, R: 5, T: 1 },
  T: { Q: 4, S: 1, U: 3 },
  U: { V: 2, W: 4 },
  V: { X: 7, Y: 3 },
  W: { G: 6 },
  X: { V: 7, Y: 1 },
  Y: { V: 3, D: 2 },
};

const graph50 = {
  A: { B: 1, C: 3, D: 7 },
  B: { A: 1, E: 2, F: 4 },
  C: { A: 3, F: 1, G: 4 },
  D: { A: 7, G: 2, H: 5 },
  E: { B: 2, H: 5, I: 3 },
  F: { B: 4, C: 1, I: 3 },
  G: { C: 4, D: 2, J: 6 },
  H: { D: 5, E: 5, K: 4 },
  I: { E: 3, F: 3, L: 2, M: 3 },
  J: { G: 6, N: 5, K: 3 },
  K: { H: 4, J: 3, O: 7 },
  L: { I: 2, P: 4, M: 3 },
  M: { I: 3, L: 3, Q: 6 },
  N: { J: 5, R: 4, O: 6 },
  O: { K: 7, N: 6, S: 2 },
  P: { L: 4, T: 3, Q: 5 },
  Q: { M: 6, P: 5, U: 5 },
  R: { N: 4, V: 3, S: 7 },
  S: { O: 2, R: 7, W: 4 },
  T: { P: 3, X: 6, U: 5 },
  U: { Q: 5, T: 5, Y: 4 },
  V: { R: 3, Z: 7, W: 6 },
  W: { S: 4, V: 6, AA: 5 },
  X: { T: 6, AB: 2, Y: 4 },
  Y: { U: 4, X: 4, AC: 3, BB: 5 },
  Z: { V: 7, AD: 6, AA: 5 },
  AA: { W: 5, Z: 5, AE: 4 },
  AB: { X: 2, AF: 7, AC: 5 },
  AC: { Y: 3, AB: 5, AG: 6 },
  AD: { Z: 6, AH: 5, AE: 7 },
  AE: { AA: 4, AD: 7, AI: 3 },
  AF: { AB: 7, AJ: 2, AG: 5 },
  AG: { AC: 6, AF: 5, AK: 4 },
  AH: { AD: 5, AL: 6, AI: 4 },
  AI: { AE: 3, AH: 4, AM: 2 },
  AJ: { AF: 2, AN: 5, AK: 4 },
  AK: { AG: 4, AJ: 4, AO: 3 },
  AL: { AH: 6, AP: 7, AM: 5 },
  AM: { AI: 2, AL: 5, AQ: 5 },
  AN: { AJ: 5, AR: 4, AO: 3 },
  AO: { AK: 3, AN: 3, AS: 6 },
  AP: { AL: 7, AT: 4, AQ: 5 },
  AQ: { AM: 5, AP: 5, AU: 3 },
  AR: { AN: 4, AV: 2, AS: 4 },
  AS: { AO: 6, AR: 4, AW: 5 },
  AT: { AP: 4, AX: 3, AU: 5 },
  AU: { AQ: 3, AT: 5, AY: 6 },
  AV: { AR: 2, AZ: 4, AW: 3 },
  AW: { AS: 5, AV: 3, BA: 3 },
  AX: { AT: 3, BB: 7, AY: 4 },
  AY: { AU: 6, AX: 4, BC: 5 },
  AZ: { AV: 4, BD: 3, BA: 6 },
  BA: { AW: 3, AZ: 6, BE: 6 },
  BB: { AX: 7, BF: 5, BC: 4, Y: 5 },
  BC: { AY: 5, BB: 4, BG: 4 },
  BD: { AZ: 3, BH: 6, BE: 5, BF: 7 },
  BE: { BA: 6, BD: 5, BI: 3 },
  BF: { BB: 5, BJ: 7, BG: 2, BD: 7 },
  BG: { BC: 4, BF: 2, BK: 2 },
  BH: { BD: 6, BL: 4, BI: 5 },
  BI: { BE: 3, BH: 5, BM: 5 },
  BJ: { BF: 7, BN: 6, BK: 4 },
  BK: { BG: 2, BJ: 4, BO: 4 },
  BL: { BH: 4, BM: 6 },
  BM: { BI: 5, BL: 6 },
  BN: { BJ: 6, BO: 5 },
  BO: { BK: 4, BN: 5 },
};

function test_case(test_case_name, graph, start, end) {
  console.log(""); // to give a line gap
  // calculating execution time and memory usage
  const start_performance = performance.now();
  const startMemory = process.memoryUsage().rss; // initial memory usage
  const { distance, path } = dijkstra(graph, start, end);
  const endMemory = process.memoryUsage().rss; // final memory usage
  const end_performance = performance.now();
  const exec_time = end_performance - start_performance;

  console.log("NODE.JS Test Case: " + test_case_name);

  console.log("\nOutput:");
  console.log(`Shortest distance from ${start} to ${end}: ${distance}`);
  console.log(`Path: ${path}`);

  console.log("\nAnalytics:");
  console.log("Execution time: " + exec_time.toFixed(10) + " ms");
  const usageMemory = (endMemory - startMemory) / 1024; // in KB
  console.log(`memory usage: ${usageMemory.toFixed(4)} KB\n`);
}

test_case("10 Vertices", graph10, "A", "J");
test_case("25 Vertices", graph25, "A", "Q");
test_case("50 Vertices", graph50, "A", "BM");
