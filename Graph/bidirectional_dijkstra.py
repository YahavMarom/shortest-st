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
        self.most_recently_closed = None

        
    def degree(self, u):
        self.query_cnt += 1
        return len(self.graph.get(u, {}))
    
    def neighbor(self, u, j):
        self.query_cnt += 1
        items = list(self.graph.get(u, {}).items())
        return items[j] #v, weight

    def get_query_count(self):
        return self.query_cnt
    
    def relax_vertex(self, u):
        deg = self.degree(u)
        for j in range(deg):
            v, w = self.neighbor(u, j)
            new_dist = self.distances[u] + w
            if new_dist < self.distances[v]:
                self.distances[v] = new_dist
                self.prev[v] = u
                heapq.heappush(self.heap, (new_dist, v))
        self.closed.add(u)
        self.most_recently_closed = u
        


    



def create_transposed_graph(graph):

    transposed_graph = {}
    for vertex in graph:
        transposed_graph[vertex] = {}
    
    for vertex in graph:
        for neighbor, weight in graph[vertex].items():
            if neighbor not in transposed_graph:
                transposed_graph[neighbor] = {}
            transposed_graph[neighbor][vertex] = weight
    return transposed_graph
                

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

    #first iteration, we don't need to check anything. 
    w, fwd_vertex = heapq.heappop(fwd_run.heap)
    deg = fwd_run.degree(fwd_vertex)

    for j in range(deg):
        v, w = fwd_run.neighbor(fwd_vertex, j)
        new_dist = fwd_run.distances[fwd_vertex] + w

        if new_dist < fwd_run.distances[v]:
            fwd_run.distances[v] = new_dist
            fwd_run.prev[v] = fwd_vertex
            heapq.heappush(fwd_run.heap, (new_dist, v))

    fwd_run.closed.add(fwd_vertex)
    fwd_run.most_recently_closed = fwd_vertex

    w, bwd_vertex = heapq.heappop(bwd_run.heap)
    deg = bwd_run.degree(bwd_vertex)

    for j in range(deg):
        v, w = bwd_run.neighbor(bwd_vertex, j)
        new_dist = bwd_run.distances[bwd_vertex] + w

        if new_dist < bwd_run.distances[v]:
            bwd_run.distances[v] = new_dist
            bwd_run.prev[v] = bwd_vertex
            heapq.heappush(bwd_run.heap, (new_dist, v))
        if v in fwd_run.closed:
            path_len = bwd_run.distances[bwd_vertex] + w + fwd_run.distances[v]
            if path_len < mu:
                mu = path_len
                e_mid = (bwd_vertex, v, "b")
    bwd_run.closed.add(bwd_vertex)
    bwd_run.most_recently_closed = bwd_vertex


    while True:

        w, fwd_vertex = heapq.heappop(fwd_run.heap)
        deg = fwd_run.degree(fwd_vertex)

        for j in range(deg):
            v, w = fwd_run.neighbor(fwd_vertex, j)
            new_dist = fwd_run.distances[fwd_vertex] + w

            if new_dist < fwd_run.distances[v]:
                fwd_run.distances[v] = new_dist
                fwd_run.prev[v] = fwd_vertex
                heapq.heappush(fwd_run.heap, (new_dist, v))

            if v in bwd_run.closed:
                path_len = fwd_run.distances[fwd_vertex] + w + bwd_run.distances[v]
                if path_len < mu:
                    mu = path_len
                    e_mid = (fwd_vertex, v, "f")

        fwd_run.closed.add(fwd_vertex)
        fwd_run.most_recently_closed = fwd_vertex


        fwd_min = fwd_run.distances[fwd_run.most_recently_closed]
        bwd_min = bwd_run.distances[bwd_run.most_recently_closed] 

        if fwd_min + bwd_min >= mu:
            break
        
        #backward turn

        w, bwd_vertex = heapq.heappop(bwd_run.heap)
        deg = bwd_run.degree(bwd_vertex)

        for j in range(deg):
            v, w = bwd_run.neighbor(bwd_vertex, j)
            new_dist = bwd_run.distances[bwd_vertex] + w

            if new_dist < bwd_run.distances[v]:
                bwd_run.distances[v] = new_dist
                bwd_run.prev[v] = bwd_vertex
                heapq.heappush(bwd_run.heap, (new_dist, v))

            if v in fwd_run.closed:
                path_len = bwd_run.distances[bwd_vertex] + w + fwd_run.distances[v]
                if path_len < mu:
                    mu = path_len
                    e_mid = (fwd_vertex, v, "f")

        bwd_run.closed.add(bwd_vertex)
        bwd_run.most_recently_closed = bwd_vertex


        fwd_min = fwd_run.distances[fwd_run.most_recently_closed]
        bwd_min = bwd_run.distances[bwd_run.most_recently_closed] 

        if fwd_min + bwd_min >= mu:
            break
    
    query = fwd_run.query_cnt + bwd_run.query_cnt     
    return mu, e_mid, fwd_run, bwd_run, query







    
    





