import heapq

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

        self.distances = {vertex: float('inf') for vertex in all_vertices}
        self.prev      = {vertex: None for vertex in all_vertices}
        self.distances[source] = 0

        self.heap      = [(0, source)]
        self.closed    = set()
        self.query_cnt = 0

    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph.get(u, []))

    def neighbor(self, u, j):
        self.query_cnt += 1
        return self.graph[u][j]

    def get_query_count(self):
        return self.query_cnt


def dijkstra(Graph, source, target, undirected=True):
    fwd_run = RunDijkstra(Graph, source)

    while fwd_run.heap:
        curr_dist, curr_vertex = heapq.heappop(fwd_run.heap)
        if curr_vertex in fwd_run.closed:
            continue
        fwd_run.closed.add(curr_vertex)

        
        if curr_dist > fwd_run.distances[target]:      # instance optimal, once closing a vertex farther than t.
            break

        for j in range(fwd_run.degree(curr_vertex)):
            v, weight = fwd_run.neighbor(curr_vertex, j)
            new_dist = curr_dist + weight
            if new_dist < fwd_run.distances[v]:
                fwd_run.distances[v] = new_dist
                fwd_run.prev[v]      = curr_vertex
                heapq.heappush(fwd_run.heap, (new_dist, v))

    # reconstruct path 
    #path = []
    #node = target
    #while node is not None:
    #    path.insert(0, node)
    #    node = fwd_run.prev[node]

    return fwd_run.query_cnt, fwd_run.distances[target]

        





