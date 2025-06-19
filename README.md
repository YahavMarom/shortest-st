# Bidirectional Dijkstra, BFS

## Description
I read an article that explained the bidirectional approach of computing the shortest s-t path in graphs.
In it, they described a version of bidirectional Dijkstra/BFS that was supposed to be optimal in terms of query complexity, up to any graph, when we don't have prior knowledge of it.

## Why?
The intuition is that Dijkstra/BFS grows in "circles", and by so, when searching for the shortest path between vertices s and t, we compute more than we need for just the shortest path: we grow one large "circle" from s. However, we can grow two smaller circles around s and t and terminate when a stopping condition is met.
It seemed interesting, so I programmed it in Python. 

## The Algorithm
We are given a graph in an adjacency list representation, and we're also given query access to it: using the degree(u) function, which returns the degree of vertex u, and using neighbor(u, i), which returns the i-th edge of vertex u.
(For the directed case, we must have an inneighbor/outneighbor.)

Given a source vertex and a target vertex, we're asked to find the shortest s-t path. The main measure of complexity will be query complexity.

In the paper, the implementation is a bit different - We relax an edge from our current vertex in the forward run (from s to t), and then we relax an edge on the transposed graph (that is, the backward run - from t to s). 

I implemented the algorithm by relaxing all edges for my current vertex in the forward run and then relaxing all edges in the backward run. Notice that up until we find the actual shortest path, we relax all edges from a vertex; it is just the last two vertices, in the forward and backward runs, where we might not relax all their edges. However, on huge graphs, that's pretty negligible in terms of query/time complexity. 

## Results
For the weighted case, I choose weights randomly chosen in [10, 500], and chose s, t randomly. I 
For the unweighted case, I made a connected graph, and had the option of adding a parameter "k" - larger k means, mostly, more edges for each vertex. Chose s,t randomly again.


### Dijkstra
In graphs where each vertex has at most 40 edges (outgoing + ingoing), Bidirectional Dijkstra was much better in terms of query complexity, and was similar to the other two in terms of time performance.

On cliques, it had performed much worse than the other two - probably because of the two heaps (When choosing s be the (n/3)th vertex, and t (2n/3)th vertex. )

### BFS
For BFS, the bidirectional approach was better as well in terms of query complexity, and its time performance was similar to the regular approach.


These suggest that on sparse graphs, the bidirectional approach can be a suitable alternative to the regular approach (well, A* still outperforms it, for weighted graphs).

The images are in the respective folders.




