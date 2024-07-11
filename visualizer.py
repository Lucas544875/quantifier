from collections import deque
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import json
from quantifier import unify, qs_to_str, level, replace_A8, replace_E8, Quantifier

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
    heirarchy = ("S", '3')
    with open("output.json", "r") as f:
        nodes, rels = json.load(f)
    nodes = [Quantifier(node) for node in nodes]
    rels = [(Quantifier(p), Quantifier(q)) for p,q in rels]
    print([(node, node.classify()) for node in nodes])
    print(rels)
    Graph = nx.DiGraph()
    for n in nodes:
        print(n, n.classify())
        if n.classify() == heirarchy:
            print(n)
            Graph.add_node(str(n.unify()))

    for (ps1, ps2) in rels:
        if ps1.classify() == heirarchy and ps2.classify() == heirarchy:
            Graph.add_edge(str(ps1.unify()), str(ps2.unify()))

    # rels = [(qs_to_str(unify(q)), qs_to_str(unify(p))) for (p,q) in rels]
    # rels = list(set(rels))
    # for (qs1, qs2) in rels:
    #     Graph.add_edge(qs1, qs2)


    sccs = list(nx.strongly_connected_components(Graph))
    cg = nx.condensation(Graph, sccs)
    cg = nx.transitive_reduction(cg)
    names = {node : ", ".join(sccs[node]) for node in cg.nodes}
    nx.draw_networkx(cg, pos=nx.nx_agraph.pygraphviz_layout(cg, prog='dot'), with_labels=True, labels=names,node_size=800)
    plt.show()
    # cg = nx.relabel_nodes(cg, names)
    # g = nx.nx_agraph.to_agraph(cg)
    
    # g.draw('sigma3-c.png',prog='dot')
