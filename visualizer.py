from collections import deque
import networkx as nx
import itertools
import json
from quantifier import unify, qs_to_str, level, replace_A8, replace_E8

def classify(qs):
    clas = ""
    if qs == []:
        clas = "C"
    elif qs[0] == "E" or qs[0] == "A8":
        clas = "Σ"
    elif qs[0] == "A" or qs[0] == "E8":
        clas = "Π"
    return clas+str(level(qs))

def quantifier_filter(qs,clas):
    return classify(qs) == clas

if __name__ == "__main__":
    with open("output.json", "r") as f:
        nodes, rels = json.load(f)

    Graph = nx.DiGraph()
    for n in nodes:
        if quantifier_filter(n,"Σ2"):
            Graph.add_node(qs_to_str(unify(n)))

    for (ps1, ps2) in rels:
        if quantifier_filter(ps1,"Σ2") and quantifier_filter(ps2,"Σ2"):
            Graph.add_edge(qs_to_str(unify(ps1)), qs_to_str(unify(ps2)))

    # rels = [(qs_to_str(unify(q)), qs_to_str(unify(p))) for (p,q) in rels]
    # rels = list(set(rels))
    # for (qs1, qs2) in rels:
    #     Graph.add_edge(qs1, qs2)


    sccs = list(nx.strongly_connected_components(Graph))
    cg = nx.condensation(Graph, sccs)
    names = {}
    for node in cg.nodes:
        names[node] = ", ".join(sccs[node])
    cg = nx.relabel_nodes(cg, names)
    g = nx.nx_agraph.to_agraph(cg)
    g.draw('sigma3-c.png',prog='dot')
