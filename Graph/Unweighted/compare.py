import random
random.seed(42)
from collections import defaultdict
import bfs
import bidirectional_bfs as bd_bfs
import time
import matplotlib.pyplot as plt



def create_transposed_graph(graph):
    transposed_graph = {u:[] for u in graph}
    for u, neighbors in graph.items():
        for v in neighbors:
            if v not in transposed_graph:
                transposed_graph[v] = []
            transposed_graph[v].append(u)
    return transposed_graph


  




def compare(tests, k, directed=True):
    

    bfs_time = []
    bfs_queries = []

    bd_bfs_time = []
    bd_bfs_queries = []
    

    for test in tests:
            
        if not directed:
            r_graph = bd_bfs.random_undirected_unweighted_graph(test, k)
        else: 
            r_graph = bd_bfs.random_directed_unweighted_graph(test, k)
        
        s, t = random.sample(range(test), 2)
        print(f"s = {s}, t = {t}")
    
        start = time.time()
        bfs_runner = bfs.RunBFS(r_graph, s)
        bfs_mu, bfs_query, prev = bfs_runner.bfs(s, t)
        end = time.time()

        time1 = round(end-start, 3)
        print(f"for regular bfs, test = {test}, mu is {bfs_mu}, query is {bfs_query}, and it took {time1} seconds")
        bfs_time.append(time1)
        bfs_queries.append(bfs_query)
        

        start = time.time()
        bd_bfs_mu, bd_bfs_query = bd_bfs.bidirectional(r_graph, s, t, directed)
        end = time.time()
        time2 = round(end-start, 3)
        print(f"for bidirectional bfs, test = {test}, mu is {bd_bfs_mu}, query is {bd_bfs_query}, and it took {time2} seconds")
        bd_bfs_time.append(time2)
        bd_bfs_queries.append(bd_bfs_query)
        if bfs_mu != bd_bfs_mu:
            break

       
        print("\n")
    return bfs_time, bfs_queries, bd_bfs_time, bd_bfs_queries


if __name__ == "__main__":
    x = [i for i in range(10, 250020, 5000)]
    K = [1, 2, 3]
    for k in K:
        bfs_time, bfs_queries, bd_bfs_time, bd_bfs_queries = compare(x, k, True)
        
        


        toggle = 1

        if toggle:
            # time plot
            fig, time_plot = plt.subplots(figsize=(6, 4), layout='constrained')
            time_plot.scatter(x, bfs_time, label='BFS')
            time_plot.scatter(x, bd_bfs_time, label='Bidirectional BFS')
            time_plot.set_xlabel('Size of Graph')
            time_plot.set_ylabel('Time (s)')
            time_plot.set_title(f"Time vs Graph Size (Directed, Unweighted), k = {k}")
            time_plot.legend()

            # query plot
            fig, query_plot = plt.subplots(figsize=(6, 4), layout='constrained')
            query_plot.scatter(x, bfs_queries, label='BFS')
            query_plot.scatter(x, bd_bfs_queries, label='Bidirectional BFS')
            query_plot.set_xlabel('Size of Graph')
            query_plot.set_ylabel('Number of Queries')
            query_plot.set_title(f"Queries vs Graph Size (Directed, Unweighted), k = {k}")
            query_plot.legend()

            plt.show()
