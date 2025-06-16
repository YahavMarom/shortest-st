import heapq


class RunDijkstra:

    def __init__(self, Graph, source):

        all_vertices = set(Graph.keys())
        for neighbors in Graph.values():
            all_vertices.update(neighbors.keys())
            
        self.graph = Graph                
        self.distances = {vertex : float('inf') for vertex in all_vertices} 
        self.distances[source] = 0           
        self.heap = [(0, source)]             
        self.closed = set()                 
        self.prev = {vertex: None for vertex in all_vertices} 
        self.query_cnt = 0

    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph.get(u, {}))
    
    def neighbor(self, u, j):
        self.query_cnt += 1
        items = list(self.graph.get(u, {}).items())
        v, weight = items[j]
        return v, weight

    def get_query_count(self):
        return self.query_cnt


def dijkstra(Graph, source, target, undirected=True):
    fwd_run = RunDijkstra(Graph, source)

    while fwd_run.heap:
        curr_dist, curr_vertex = heapq.heappop(fwd_run.heap)
        fwd_run.closed.add(curr_vertex)

        if curr_dist > fwd_run.distances[target]:      # instance optimal, once closing a vertex farther than t.
            break
        #if curr_dist > fwd_run.distances[curr_vertex]:
        #    continue
        curr_deg_of_vertex = fwd_run.degree(curr_vertex)

        for j in range(curr_deg_of_vertex):
            neighbor, l_uv = fwd_run.neighbor(curr_vertex, j)
            new_dist = curr_dist + l_uv
            if new_dist < fwd_run.distances[neighbor]:
                fwd_run.distances[neighbor] = new_dist
                heapq.heappush(fwd_run.heap, (new_dist, neighbor))
                fwd_run.prev[neighbor] = curr_vertex
    path = []
    current = target
    while current is not None:
        path.insert(0, current)
        current = fwd_run.prev[current]

    return fwd_run.query_cnt, fwd_run.distances[target]
                  





