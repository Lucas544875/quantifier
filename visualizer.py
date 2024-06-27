from collections import deque
import networkx as nx
import itertools

if __name__ == "__main__":
    f = open("output.txt", "r")
    lines = f.readlines()
    f.close()

    Graph = nx.DiGraph()
    for line in lines:
        v = line.split()
        Graph.add_edge(v[0], v[1])

    sccs = list(nx.strongly_connected_components(Graph))
    cg = nx.condensation(Graph, sccs)
    names = {}
    for node in cg.nodes:
        names[node] = ", ".join(sccs[node])
    # print(names)
    cg = nx.relabel_nodes(cg, names)
    g = nx.nx_agraph.to_agraph(cg)
    g.draw('sigma3-c.png',prog='dot')
