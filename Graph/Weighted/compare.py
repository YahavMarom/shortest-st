import bidirectional_dijkstra
import dijkstra
import improved_dijk as improved
import random
import time
import matplotlib.pyplot as plt
import numpy as np
random.seed(42)




def undirected_random_graph_generator(n):
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(i+1,n):
            if i != j:
                graph[i][j] = random.randint(10, 1000)
                graph[j][i] = graph[i][j]
                
    return graph



#directed

def directed_random_graph_generator(n):
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = random.randint(10, 1000)
                
    return graph

def compare(tests, undirected):
    

    
    dijk_time = []
    dijk_queries = []

    improv_time = []
    improv_queries = []


    bd_dijk_time = []
    bd_dijk_queries = []

    for test in tests:
        if undirected:
            r_graph = undirected_random_graph_generator(test)
        else: 
            r_graph = directed_random_graph_generator(test)
        
        s, t = round(test / 3), round (test * 2 / 3)

        start = time.time()
        dijk_query, dijk_mu = dijkstra.dijkstra(r_graph, s, t)
        end = time.time()
        time1 = round(end-start, 3)
        print(f"for regular dijk, test = {test}, mu is {dijk_mu}, query is {dijk_query}, and it took {time1} seconds")
        dijk_time.append(time1)
        dijk_queries.append(dijk_query)

        start = time.time()
        improved_dijk_query, improved_dijk_mu = improved.dijkstra(r_graph, s, t)
        end = time.time()
        time2 = round(end-start, 3)
        print(f"for improved dijk, test = {test}, mu is {improved_dijk_mu}, query is {improved_dijk_query}, and it took {time2} seconds")
        improv_time.append(time2)
        improv_queries.append(improved_dijk_query)

        start = time.time()
        mu, e_mid, fwd_run, bwd_run, query = bidirectional_dijkstra.bidirectional(r_graph, s, t, undirected)
        end = time.time()
        time3 = round(end-start, 3)
        print(f"for bidirectional dijk, test = {test} mu is {mu}, query is {query}, and it took {time3} seconds")
        bd_dijk_time.append(time3)
        bd_dijk_queries.append(query)
        print("\n")
    return dijk_time, dijk_queries, improv_time, improv_queries, bd_dijk_time, bd_dijk_queries


if __name__ == "__main__":
    x = [50 * i for i in range(1, 2)] 
    dijk_time, dijk_queries, improv_time, improv_queries, bd_dijk_time, bd_dijk_queries = compare(x, True)
    


    toggle = 1
    if toggle:
        fig, time_plot = plt.subplots(figsize=(6, 4), layout='constrained')
        time_plot.plot(x, dijk_time, label='Dijkstra')
        time_plot.plot(x, improv_time, label='Improved Dijkstra')
        time_plot.plot(x, bd_dijk_time, label='Bidirectional Dijkstra')
        time_plot.set_xlabel('Size of Clique')
        time_plot.set_ylabel('Time (s)')
        time_plot.set_title("Time vs Clique Size (Undirected, Weighted)")
        time_plot.legend()

        # query plot
        fig, query_plot = plt.subplots(figsize=(6, 4), layout='constrained')
        query_plot.plot(x, dijk_queries, label='Dijkstra')
        query_plot.plot(x, improv_queries, label='Improved Dijkstra')
        query_plot.plot(x, bd_dijk_queries, label='Bidirectional Dijkstra')
        query_plot.set_xlabel('Size of Clique')
        query_plot.set_ylabel('Number of Queries')
        query_plot.set_title("Queries vs Clique Size (Undirected, Weighted)")
        query_plot.legend()

        plt.show()







