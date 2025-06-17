import heapq
import random
random.seed(42)

class RunDijkstra:
    def __init__(self, Graph, source):
        
        self.graph = {}
        for u, nbrs in Graph.items():
            if isinstance(nbrs, dict):
                self.graph[u] = list(nbrs.items())
            else:
                
                self.graph[u] = nbrs

        
        all_vertices = set(self.graph.keys())
        for nbr_list in self.graph.values():
            for v, _ in nbr_list:
                all_vertices.add(v)

        
        self.distances = {v: float('inf') for v in all_vertices}
        self.prev = {v: None for v in all_vertices}
        self.distances[source] = 0

        self.heap = [(0, source)]
        self.closed = set()
        self.query_cnt = 0
        self.most_recently_closed = None

    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph.get(u, []))
    
    def neighbor(self, u, j):
        self.query_cnt += 1
        return self.graph[u][j]  # (v, weight)

    def get_query_count(self):
        return self.query_cnt
    
    def relax_vertex(self, u):
        
        for j in range(self.degree(u)):
            v, w = self.neighbor(u, j)
            new_dist = self.distances[u] + w
            if new_dist < self.distances[v]:
                self.distances[v] = new_dist
                self.prev[v] = u
                heapq.heappush(self.heap, (new_dist, v))
        self.closed.add(u)
        self.most_recently_closed = u


def create_transposed_graph(graph):
    
    transposed = {}
    for u, nbrs in graph.items():
        
        transposed.setdefault(u, {})
        
        items = nbrs.items() if isinstance(nbrs, dict) else nbrs
        for v, w in items:
            transposed.setdefault(v, {})
            transposed[v][u] = w
    return transposed


def bidirectional(graph, source, target, undirected=True):
    if source == target:
        return 0, None, None, None

    fwd_run = RunDijkstra(graph, source)
    if undirected:
        bwd_run = RunDijkstra(graph, target)
    else:
        bwd_run = RunDijkstra(create_transposed_graph(graph), target)

    mu = float('inf')
    e_mid = None

    
    w1, u = heapq.heappop(fwd_run.heap)
    fwd_run.relax_vertex(u)
    
    w2, u_b = heapq.heappop(bwd_run.heap)
    bwd_run.relax_vertex(u_b)
    
    for v, w_uv in bwd_run.graph[u_b]:
        if v in fwd_run.closed:
            path_len = bwd_run.distances[u_b] + w_uv + fwd_run.distances[v]
            if path_len < mu:
                mu = path_len
                e_mid = (u_b, v, 'b')

    # main loop
    while True:
        # forward turn
        w1, u_f = heapq.heappop(fwd_run.heap)
        fwd_run.relax_vertex(u_f)
        for v, w_uv in fwd_run.graph[u_f]:
            if v in bwd_run.closed:
                path_len = fwd_run.distances[u_f] + w_uv + bwd_run.distances[v]
                if path_len < mu:
                    mu = path_len
                    e_mid = (u_f, v, 'f')

        # stopping condition
        fwd_min = fwd_run.distances[fwd_run.most_recently_closed]
        bwd_min = bwd_run.distances[bwd_run.most_recently_closed]
        if fwd_min + bwd_min >= mu:
            break

        # backward turn
        w2, u_b = heapq.heappop(bwd_run.heap)
        bwd_run.relax_vertex(u_b)
        for v, w_uv in bwd_run.graph[u_b]:
            if v in fwd_run.closed:
                path_len = bwd_run.distances[u_b] + w_uv + fwd_run.distances[v]
                if path_len < mu:
                    mu = path_len
                    e_mid = (u_b, v, 'b')

        fwd_min = fwd_run.distances[fwd_run.most_recently_closed]
        bwd_min = bwd_run.distances[bwd_run.most_recently_closed]
        if fwd_min + bwd_min >= mu:
            break

    query = fwd_run.get_query_count() + bwd_run.get_query_count()
    return mu, e_mid, fwd_run, bwd_run, query


def random_graph_generator(n):
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            w = random.randint(10, 100)
            graph[i][j] = w
            graph[j][i] = w
    return graph
