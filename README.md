# Bidirectional Dijkstra

## Description
I read an article by [Richard Hladík and others](https://arxiv.org/abs/2410.14638) that explained the bidirectional approach of computing the shortest st-path in graphs.
In it, they described a version of bidirectional Dijkstra/BFS that was supposed to be optimal, up to any kind of graph, when we don't have prior knowledge of it.

## Why?
The intuition is that Dijkstra/BFS grow in "circles", and by so, when searching for the shortes path between vertices s and t, we compute more than we're needed for just the shortest path: we grow one large "circle" from s. However, we can grow two, smaller, circles around s and t and terminate when a stopping condition is met.
It seemed interesting, so I programmed it in Python. 
Not so surprising, the Bidirectional Dijkstra outperformed Dijkstra (and also an improvement of Dijkstra). 

