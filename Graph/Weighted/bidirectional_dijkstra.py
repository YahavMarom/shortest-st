import heapq
import random
random.seed(42)

class RunDijkstra:
    def __init__(self, Graph, source, backward=False):
        self.graph = {}

        if isinstance(Graph, dict) and 'outneighbors' in Graph and 'inneighbors' in Graph:
            raw_graph = Graph['inneighbors'] if backward else Graph['outneighbors']
        else:
            raw_graph = Graph

        for u, nbrs in raw_graph.items():
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


def bidirectional(graph, source, target, undirected=True):
    if source == target:
        return 0, None, None, None

    fwd_run = RunDijkstra(graph, source, backward=False)
    if undirected:
        bwd_run = RunDijkstra(graph, target, backward=False)
    else:
        bwd_run = RunDijkstra(graph, target, backward=True)

    mu = float('inf')
    e_mid = None

    if fwd_run.heap:
        w1, u = heapq.heappop(fwd_run.heap)
        fwd_run.relax_vertex(u)

    if bwd_run.heap:
        w2, u_b = heapq.heappop(bwd_run.heap)
        bwd_run.relax_vertex(u_b)

        for v, w_uv in bwd_run.graph[u_b]:
            if v in fwd_run.closed:
                path_len = bwd_run.distances[u_b] + w_uv + fwd_run.distances[v]
                if path_len < mu:
                    mu = path_len
                    e_mid = (u_b, v, 'b')

    while fwd_run.heap and bwd_run.heap:
        # forward turn
        w1, u_f = heapq.heappop(fwd_run.heap)
        fwd_run.relax_vertex(u_f)
        for v, w_uv in fwd_run.graph[u_f]:
            if v in bwd_run.closed:
                path_len = fwd_run.distances[u_f] + w_uv + bwd_run.distances[v]
                if path_len < mu:
                    mu = path_len
                    e_mid = (u_f, v, 'f')

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


def random_directed_graph_generator(n, min_out=4, max_out=20, min_w=10, max_w=1000):
    out = {i: {} for i in range(n)}

    for i in range(n):
        v = (i + 1) % n
        w = random.randint(min_w, max_w)
        out[i][v] = w

    for u in range(n):
        existing = set(out[u].keys()) | {u, (u + 1) % n}
        num_additional = random.randint(min_out, max_out) - 1
        possible_targets = list(set(range(n)) - existing)
        random.shuffle(possible_targets)
        for v in possible_targets[:num_additional]:
            w = random.randint(min_w, max_w)
            out[u][v] = w

    inn = {i: {} for i in range(n)}
    for u, neighbors in out.items():
        for v, w in neighbors.items():
            inn[v][u] = w

    return {
        'outneighbors': sort_dict_values(out),
        'inneighbors': sort_dict_values(inn)
    }

def sort_dict_values(d):
    return {k: dict(sorted(v.items())) for k, v in d.items()}

def random_undirected_graph_generator(n, min_out=4, max_out=20, min_w=10, max_w=1000):
    graph = {i: {} for i in range(n)}

    for i in range(n):
        u = i
        v = (i + 1) % n
        w = random.randint(min_w, max_w)
        graph[u][v] = w
        graph[v][u] = w

    for u in range(n):
        existing = set(graph[u].keys()) | {u, (u + 1) % n}
        num_additional = random.randint(min_out, max_out) - 1
        possible_targets = list(set(range(n)) - existing)
        random.shuffle(possible_targets)
        for v in possible_targets[:num_additional]:
            w = random.randint(min_w, max_w)
            graph[u][v] = w
            graph[v][u] = w

    return sort_dict_values(graph)