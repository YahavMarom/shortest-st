import collections
import random
from collections import defaultdict
random.seed(42)


class RunBFS:
    def __init__(self, Graph, source):
        # Convert graph to adjacency list format
        self.graph = {}
        for u, nbrs in Graph.items():
            if isinstance(nbrs, dict):  
                self.graph[u] = list(nbrs.keys())
            else:
                self.graph[u] = nbrs

        # Ensure all vertices exist in the graph
        all_vertices = set(self.graph.keys())
        for nbr_list in self.graph.values():
            all_vertices.update(nbr_list)
        for v in all_vertices:
            self.graph.setdefault(v, [])

        self.queue = collections.deque([source])
        self.closed = {source}         # mark source as seen
        self.prev = {source: None}
        self.distances = {source: 0}        # distance from source
        self.query_cnt = 0
        self.most_recently_closed = source
        
    def get_query_count(self):
        return self.query_cnt

    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph.get(u, []))

    def neighbor(self, u, j):
        self.query_cnt += 1
        return self.graph[u][j]
    
    def relax_vertex(self, u):
        for j in range(self.degree(u)):
            v = self.neighbor(u, j)
            if v not in self.closed:  # Only process unvisited neighbors
                self.distances[v] = self.distances[u] + 1
                self.prev[v] = u
                self.queue.append(v)
                self.closed.add(v)
        self.most_recently_closed = u


def bidirectional(graph, source, target, undirected=True):
    if source == target:
        return 0, 0, [source]
    
    fwd_run = RunBFS(graph, source)
    if undirected:
        bwd_run = RunBFS(graph, target)
    else:
        bwd_run = RunBFS(create_transposed_graph(graph), target)
    
    mu = float('inf')
    e_mid = None

    while fwd_run.queue and bwd_run.queue:
        # Forward step
        if fwd_run.queue:
            u_f = fwd_run.queue.popleft()
            fwd_run.relax_vertex(u_f)
            
            # Check for intersection after relaxing forward vertex
            for j in range(fwd_run.degree(u_f)):
                v = fwd_run.neighbor(u_f, j)
                if v in bwd_run.closed:
                    path_len = fwd_run.distances[u_f] + 1 + bwd_run.distances[v]
                    if path_len < mu:
                        mu = path_len
                        e_mid = (u_f, v, 'f')

        # Check stopping condition
        if fwd_run.most_recently_closed in fwd_run.distances and bwd_run.most_recently_closed in bwd_run.distances:
            fwd_min = fwd_run.distances[fwd_run.most_recently_closed]
            bwd_min = bwd_run.distances[bwd_run.most_recently_closed]
            if fwd_min + bwd_min >= mu:
                break

        # Backward step
        if bwd_run.queue:
            u_b = bwd_run.queue.popleft()
            bwd_run.relax_vertex(u_b)
            
            # Check for intersection after relaxing backward vertex
            for j in range(bwd_run.degree(u_b)):
                v = bwd_run.neighbor(u_b, j)
                if v in fwd_run.closed:
                    path_len = bwd_run.distances[u_b] + 1 + fwd_run.distances[v]
                    if path_len < mu:
                        mu = path_len
                        e_mid = (u_b, v, 'b')

        # Check stopping condition again
        if fwd_run.most_recently_closed in fwd_run.distances and bwd_run.most_recently_closed in bwd_run.distances:
            fwd_min = fwd_run.distances[fwd_run.most_recently_closed]
            bwd_min = bwd_run.distances[bwd_run.most_recently_closed]
            if fwd_min + bwd_min >= mu:
                break

    if mu == float('inf'):
        return -1, fwd_run.get_query_count() + bwd_run.get_query_count(), []
    
    query_count = fwd_run.get_query_count() + bwd_run.get_query_count()
    return mu, query_count



def create_transposed_graph(graph):
    transposed_graph = {u: [] for u in graph}
    for u, neighbors in graph.items():
        for v in neighbors:
            if v not in transposed_graph:
                transposed_graph[v] = []
            transposed_graph[v].append(u)
    return transposed_graph


def random_directed_unweighted_graph(n, k):
    graph = defaultdict(set)

    for i in range(n):
        graph[i].add((i + 1) % n)

    for u in range(n):
        while len(graph[u]) < k + 1: 
            v = random.randint(0, n - 1)
            if v != u:
                graph[u].add(v)

    return {u: sorted(graph[u]) for u in range(n)}


def random_undirected_unweighted_graph(n, k):
    graph = defaultdict(set)

    nodes = list(range(n))
    random.shuffle(nodes)
    for i in range(1, n):
        u = nodes[i]
        v = nodes[random.randint(0, i - 1)]
        graph[u].add(v)
        graph[v].add(u)

    for u in range(n):
        while len(graph[u]) < k + 1:  
            v = random.randint(0, n - 1)
            if v != u and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)

    return {u: sorted(graph[u]) for u in range(n)}

