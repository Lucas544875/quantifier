from collections import deque
import networkx as nx
import itertools
import json
from quantifier import unify, qs_to_str, level

if __name__ == "__main__":
    with open("output.json", "r") as f:
        nodes, rels = json.load(f)
    rels = [(qs_to_str(unify(q)), qs_to_str(unify(p))) for (p,q) in rels]
    rels = list(set(rels))
    Graph = nx.DiGraph()
    for (qs1, qs2) in rels:
        Graph.add_edge(qs1, qs2)

    sccs = list(nx.strongly_connected_components(Graph))
    cg = nx.condensation(Graph, sccs)
    names = {}
    for node in cg.nodes:
        names[node] = ", ".join(sccs[node])
    cg = nx.relabel_nodes(cg, names)
    g = nx.nx_agraph.to_agraph(cg)
    g.draw('sigma3-c.png',prog='dot')
