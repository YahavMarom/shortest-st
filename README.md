# Bidirectional Dijkstra

## Description
I read an article that explained the bidirectional approach of computing the shortest s-t path in graphs.
In it, they described a version of bidirectional Dijkstra/BFS that was supposed to be optimal in terms of query complexity, up to any graph, when we don't have prior knowledge of it.

## Why?
The intuition is that Dijkstra/BFS grows in "circles", and by so, when searching for the shortest path between vertices s and t, we compute more than we need for just the shortest path: we grow one large "circle" from s. However, we can grow two smaller circles around s and t and terminate when a stopping condition is met.
It seemed interesting, so I programmed it in Python. 

## The Algorithm
We are given a graph in an adjacency list representation, and we're also given query access to it: using the degree(u) function, which returns the degree of vertex u, and using neighbor(u, i), which returns the i-th edge of vertex u.

Given a source vertex and a target vertex, we're asked to find the shortest s-t path. The main measure of complexity will be query complexity.

In the paper, the implementation is a bit different - We relax an edge from our current vertex in the forward run (from s to t), and then we relax an edge on the transposed graph (that is, the backward run - from t to s). 

I implemented the algorithm by relaxing all edges for my current vertex in the forward run and then relaxing all edges in the backward run. Notice that up until we find the actual shortest path, we relax all edges from a vertex; it is just the last two vertices, in the forward and backward runs, where we might not relax all their edges. However, on huge graphs, that's pretty negligible in terms of query/time complexity. 

## Graphs
I choose, for cliques of large sizes with weights randomly chosen in [10, 1000], for the source to be the |size|/3-th vertex, target to be the |size|*2/3-th vertex.

It seems that, in terms of query complexity, Bidirectional Dijkstra is significantly better than the other two. In terms of time complexity, it appears it performs much worse. That's most likely because of the two heaps and needing to perform more code operations. 

Improved Dijkstra fluctuates a lot, as you will see. For the time complexity, that's most likely because of the if-statement, since on large graphs, doing that lots of times adds up. For queries, I'm not entirely sure.
(Will add later on graphs comparing the unweighted case/A*)

![query_dijkstra](https://github.com/user-attachments/assets/becc96e6-6487-4082-abf7-9253fa19fd22)
![time_dijkstra](https://github.com/user-attachments/assets/e7ed0c0a-57b6-4516-abc6-5681a6ce885a)




