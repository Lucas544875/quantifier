from collections import deque
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import json
from quantifier import unify, qs_to_str, level, replace_A8, replace_E8, Quantifier

if __name__ == "__main__":
    heirarchy = ("S", '3')
    with open("output.json", "r") as f:
        nodes, rels = json.load(f)
    nodes = [Quantifier(node) for node in nodes]
    rels = [(Quantifier(q), Quantifier(p)) for p,q in rels]
    Graph = nx.DiGraph()
    for n in nodes:
        if n.classify() == heirarchy:
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
    nx.draw_networkx(cg, pos=nx.nx_agraph.pygraphviz_layout(cg, prog='dot'), with_labels=True, labels=names,node_size=2000)
    plt.savefig("sigma3-c.png")
    plt.show()
    # cg = nx.relabel_nodes(cg, names)
    # g = nx.nx_agraph.to_agraph(cg)
    
    # g.draw('sigma3-c.png',prog='dot')
