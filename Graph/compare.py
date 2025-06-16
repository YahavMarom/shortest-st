import bidirectional_dijkstra 
import dijkstra as dijkstra
import improved_dijkstra as improved
import random
import time
random.seed(42)
tests = [5, 10, 25, 50, 100]

def random_graph_generator(n):
    graph = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = random.randint(1, 500)
                
    return graph



if __name__ == "__main__":
    toggle = 1
    r_graph = random_graph_generator(5)
    if toggle:
        for test in tests:
            r_graph = random_graph_generator(test)

            s, t = round(test / 3), round (test * 2 / 3)

            start = time.time()
            dijk_query, dijk_mu = dijkstra.dijkstra(r_graph, s, t)
            end = time.time()
            print(f"for regular dijk, test = {test}, mu is {dijk_mu}, query is {dijk_query}, and it took {round(end-start, 3)} second")


            start = time.time()
            improved_dijk_query, improved_dijk_mu = improved.dijkstra(r_graph, s, t)
            end = time.time()
            print(f"for improved dijk, test = {test}, mu is {improved_dijk_mu}, query is {improved_dijk_query}, and it took {round(end-start, 3)} second")


            start = time.time()
            mu, e_mid, fwd_run, bwd_run, query = bidirectional_dijkstra.bidirectional(r_graph, s, t, False)
            end = time.time()
            print(f"for bidirectional dijk, test = {test} mu is {mu}, query is {query}, and it took {round(end-start, 3)} second")
            print("\n")


   



