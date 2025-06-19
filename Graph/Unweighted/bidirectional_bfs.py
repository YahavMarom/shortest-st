import collections
import random
from collections import defaultdict

random.seed(42)

def random_directed_unweighted_graph(n, k):
    
    out = defaultdict(set)
    for i in range(n):
        out[i].add((i + 1) % n)
    for u in range(n):
        while len(out[u]) < k + 1:
            v = random.randrange(n)
            if v != u:
                out[u].add(v)
    inn = defaultdict(set)
    for u, nbrs in out.items():
        for v in nbrs:
            inn[v].add(u)
    for i in range(n):
        out.setdefault(i, set())
        inn.setdefault(i, set())
    return {
        'outneighbors': {u: sorted(out[u]) for u in range(n)},
        'inneighbors':  {u: sorted(inn[u]) for u in range(n)},
    }

def random_undirected_unweighted_graph(n, k):
    graph = defaultdict(set)
    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randrange(i)]
        graph[u].add(v)
        graph[v].add(u)
    for u in range(n):
        while len(graph[u]) < k + 1:
            v = random.randrange(n)
            if v != u and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
    return {u: sorted(graph[u]) for u in range(n)}

def create_transposed_graph(adj):
    T = {u: [] for u in adj}
    for u, nbrs in adj.items():
        for v in nbrs:
            T.setdefault(v, []).append(u)
    return {u: sorted(neigh) for u, neigh in T.items()}

class RunBFS:
    def __init__(self, Graph, source, incoming=False):
        
        if isinstance(Graph, dict) and 'outneighbors' in Graph and 'inneighbors' in Graph:
            self.graph = (Graph['inneighbors'] if incoming 
                          else Graph['outneighbors'])
        else:
            
            self.graph = {u: list(nbrs) for u, nbrs in Graph.items()}

        
        all_vs = set(self.graph)
        for nbrs in self.graph.values():
            all_vs.update(nbrs)
        for v in all_vs:
            self.graph.setdefault(v, [])

        
        self.queue = collections.deque([source])
        self.closed = {source}
        self.prev = {source: None}
        self.distances = {source: 0}
        self.query_cnt = 0
        self.most_recently_closed = source

    def get_query_count(self):
        return self.query_cnt

    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph[u])

    def neighbor(self, u, j):
        self.query_cnt += 1
        return self.graph[u][j]

    def relax_vertex(self, u):
        for j in range(self.degree(u)):
            v = self.neighbor(u, j)
            if v not in self.closed:
                self.distances[v] = self.distances[u] + 1
                self.prev[v] = u
                self.queue.append(v)
                self.closed.add(v)
        self.most_recently_closed = u

def bidirectional(graph, source, target, directed=False):
    if source == target:
        return 0, 0, [source]

    # forward always on out-edges
    fwd = RunBFS(graph, source, incoming=False)
    # backward on in-edges if directed, else also on out-edges
    bwd = RunBFS(graph, target, incoming=directed)

    mu = float('inf')
    e_mid = None

    while fwd.queue and bwd.queue:
        # ---- forward step ----
        u = fwd.queue.popleft()
        fwd.relax_vertex(u)
        for j in range(fwd.degree(u)):
            v = fwd.neighbor(u, j)
            if v in bwd.closed:
                dist = fwd.distances[u] + 1 + bwd.distances[v]
                if dist < mu:
                    mu = dist
                    e_mid = ('fwd', u, v)

        # stopping check
        if (fwd.distances[fwd.most_recently_closed] +
            bwd.distances[bwd.most_recently_closed] >= mu):
            break

        # ---- backward step ----
        u = bwd.queue.popleft()
        bwd.relax_vertex(u)
        for j in range(bwd.degree(u)):
            v = bwd.neighbor(u, j)
            if v in fwd.closed:
                dist = bwd.distances[u] + 1 + fwd.distances[v]
                if dist < mu:
                    mu = dist
                    e_mid = ('bwd', u, v)

        # stopping check
        if (fwd.distances[fwd.most_recently_closed] +
            bwd.distances[bwd.most_recently_closed] >= mu):
            break

    total_queries = fwd.get_query_count() + bwd.get_query_count()
    if mu == float('inf'):
        return -1, total_queries, []
    return mu, total_queries
