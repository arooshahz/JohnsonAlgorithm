# Johnson Algorithm

The Johnson Algorithm is a graph algorithm used to find the shortest paths between all pairs of vertices in a weighted directed graph. It can handle graphs with negative edge weights, including graphs with negative cycles.

## Algorithm Overview

The Johnson Algorithm follows these steps:

1. Add a new vertex to the graph and connect it to all existing vertices with zero-weight edges. This ensures that there are no negative cycles in the graph.

2. Apply the Bellman-Ford algorithm on the modified graph to find the shortest distances from the newly added vertex to all other vertices. This step helps to detect any negative cycles in the graph.

3. Modify the original edge weights in the graph to get rid of negative weights. This modification is done using the shortest distances obtained from the Bellman-Ford algorithm.

4. Run Dijkstra's algorithm on the modified graph for each vertex as the source to find the shortest paths to all other vertices. Dijkstra's algorithm is applied multiple times, once for each vertex in the graph.
