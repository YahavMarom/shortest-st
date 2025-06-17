# Bidirectional Dijkstra

## Description
I read an article by [Richard Hladík and others](https://arxiv.org/abs/2410.14638) that explained the bidirectional approach of computing the shortest st-path in graphs.
In it, they described a version of bidirectional Dijkstra/BFS that was supposed to be optimal, up to any graph, when we don't have prior knowledge of it.

## Why?
The intuition is that Dijkstra/BFS grows in "circles", and by so, when searching for the shortest path between vertices s and t, we compute more than we need for just the shortest path: we grow one large "circle" from s. However, we can grow two smaller circles around s and t and terminate when a stopping condition is met.
It seemed interesting, so I programmed it in Python. 
Not so surprisingly, the Bidirectional Dijkstra outperformed Dijkstra (and also an improvement of Dijkstra). 

## The Algorithm
We are given a graph in an adjacency list representation, and we're also given query access to it: using the degree(u) function, which returns the degree of vertex u, and using neighbor(u, i), which returns the i-th edge of vertex u.
Given a source vertex and a target vertex, we're asked to find the shortest s-t path. The main measure of complexity will be query complexity.
In the paper, the implementation is a bit different - We relax an edge from our current vertex in the forward run (from s to t), and then we relax an edge on the transposed graph (that is, the backward run - from t to s). 
I implemented the algorithm by relaxing all edges for my current vertex in the forward run and then relaxing all edges in the backward run. Notice that up until we find the actual shortest path, we relax all edges from a vertex; it is just the last two vertices, in the forward and backward runs, where we might not relax all their edges. However, on huge graphs, that's pretty negligible in terms of query/time complexity. 

## Graphs
Here are graphs that show the comparison of Bidirectional Dijkstra, regular Dijkstra, and an improved Dijkstra.
![Query](https://raw.githubusercontent.com/YahavMarom/shortest-st/refs/heads/main/Graph/query.png)
![Time](https://raw.githubusercontent.com/YahavMarom/shortest-st/refs/heads/main/Graph/time.png)

