import bidirectional_dijkstra
import dijkstra as dijkstra
import improved_dijk as improved
import random
import time
random.seed(42)
tests = [5, 10, 25, 50, 100]




def undirected_random_graph_generator(n):
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(i+1,n):
            if i != j:
                graph[i][j] = random.randint(1, 500)
                graph[j][i] = graph[i][j]
                
    return graph



#directed

def directed_random_graph_generator(n):
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = random.randint(1, 500)
                
    return graph

def compare(tests, undirected):
    for test in tests:
        if undirected:
            r_graph = undirected_random_graph_generator(test)
        else: 
            r_graph = directed_random_graph_generator(test)
        print(r_graph)
        s, t = round(test / 3), round (test * 2 / 3)

        start = time.time()
        dijk_query, dijk_mu = dijkstra.dijkstra(r_graph, s, t)
        end = time.time()
        print(f"for regular dijk, test = {test}, mu is {dijk_mu}, query is {dijk_query}, and it took {round(end-start, 3)} seconds")


        start = time.time()
        improved_dijk_query, improved_dijk_mu = improved.dijkstra(r_graph, s, t)
        end = time.time()
        print(f"for improved dijk, test = {test}, mu is {improved_dijk_mu}, query is {improved_dijk_query}, and it took {round(end-start, 3)} seconds")


        start = time.time()
        mu, e_mid, fwd_run, bwd_run, query = bidirectional_dijkstra.bidirectional(r_graph, s, t, undirected)
        end = time.time()
        print(f"for bidirectional dijk, test = {test} mu is {mu}, query is {query}, and it took {round(end-start, 3)} seconds")
        print("\n")

if __name__ == "__main__":
    tests = [5, 10, 50, 100, 250]
    compare(tests, True)



