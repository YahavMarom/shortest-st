import collections
import random
from collections import defaultdict
random.seed(42)


class RunBFS:
    def __init__(self, Graph, source):
        if isinstance(Graph, dict) and 'outneighbors' in Graph:
            self.graph = Graph['outneighbors']
        else:
            
            if isinstance(Graph, dict) and 'inneighbors' in Graph:
                
                self.graph = {u: sorted(set(Graph['outneighbors'][u]) | set(Graph['inneighbors'][u]))
                              for u in Graph['outneighbors']}
            else:
                self.graph = {u: list(nbrs) for u, nbrs in Graph.items()}

        # Ensure all vertices exist in the graph
        all_vertices = set(self.graph.keys())
        for nbr_list in self.graph.values():
            all_vertices.update(nbr_list)
        for v in all_vertices:
            self.graph.setdefault(v, [])

        self.queue = collections.deque([source])
        self.closed = {source}         # mark source as seen
        self.prev = {source: None}
        self.dist = {source: 0}        # distance from source
        self.query_cnt = 0

    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph.get(u, []))

    def neighbor(self, u, j):
        self.query_cnt += 1
        return self.graph[u][j]

    def bfs(self, source, target):
        while self.queue:
            u = self.queue.popleft()

            if u == target:
                return self.dist[u], self.query_cnt, 0

            # Explore neighbors
            deg = self.degree(u)
            for j in range(deg):
                v = self.neighbor(u, j)
                if v not in self.closed:
                    self.closed.add(v)
                    self.queue.append(v)
                    self.prev[v] = u
                    self.dist[v] = self.dist[u] + 1



def random_directed_unweighted_graph(n, k):
    graph = defaultdict(set)

    # ensure a cycle for connectivity
    for i in range(n):
        graph[i].add((i + 1) % n)

    # add random extra edges
    for u in range(n):
        while len(graph[u]) < k + 1:
            v = random.randint(0, n - 1)
            if v != u:
                graph[u].add(v)

    return {u: sorted(graph[u]) for u in range(n)}


def random_undirected_unweighted_graph(n, k):
    graph = defaultdict(set)

    # build a random spanning tree
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        graph[u].add(v)
        graph[v].add(u)

    # add random extra edges
    for u in range(n):
        while len(graph[u]) < k + 1:
            v = random.randint(0, n - 1)
            if v != u and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)

    return {u: sorted(graph[u]) for u in range(n)}

def construct_path(prev, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev.get(current)
    path.reverse()
    if path and path[0] == source:
        return path