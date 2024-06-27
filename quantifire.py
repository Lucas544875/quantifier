from collections import deque
import networkx as nx
import itertools
# import pydot

# 量化子の列:(E, A, E8, A8)からなる配列

def quantifire_extention_init_sigma(qs, n):
    return [(qs+["E"], 1), (qs+["A8"], 2)]
def quantifire_extention_init_pi(qs, n):
    return [(qs+["A"], 1), (qs+["A8"], 2)]

def quantifire_extention_E(qs, n):
    return [(qs+["A"], n+1), (qs+["A8"], n+1), (qs+["E8"], n+2)]
def quantifire_extention_A(qs, n):
    return [(qs+["E"], n+1), (qs+["E8"], n+1), (qs+["A8"], n+2)]
def quantifire_extention_E8(qs, n):
    return [(qs+["A"], n+1), (qs+["E"], n), (qs+["E","E"], n), (qs+["A8"], n+1), (qs+["E8"], n+2)]
    # return [(qs+["A"], n+1), (qs+["E"], n), (qs+["A8"], n+1), (qs+["E8"], n+2)]
def quantifire_extention_A8(qs, n):
    return [(qs+["E"], n+1), (qs+["A"], n), (qs+["A","A"], n), (qs+["E8"], n+1), (qs+["A8"], n+2)]
    # return [(qs+["E"], n+1), (qs+["A"], n), (qs+["E8"], n+1), (qs+["A8"], n+2)]

def quantifire_extention(qs, n, clas):
    if qs == []:
        if clas == "sigma":
            return quantifire_extention_init_sigma(qs, n)
        elif clas == "pi":
            return quantifire_extention_init_pi(qs, n)
    if qs[-1] == "E":
        return quantifire_extention_E(qs, n)
    elif qs[-1] == "A":
        return quantifire_extention_A(qs, n)
    elif qs[-1] == "E8":
        return quantifire_extention_E8(qs, n)
    elif qs[-1] == "A8":
        return quantifire_extention_A8(qs, n)
    
def generate_qutantifire(n, clas):
    quanifires = []
    q = deque()
    q.append(([], 0)) #computable ralationから始める
    while len(q) > 0:
        qs, m = q.popleft()
        if m <= n:
            quanifires.append(qs)  # class n以下なら量化子列を枚挙
            q.extend(quantifire_extention(qs, m, clas)) # 後ろにくっつけて延長した量化子列を生成
    return quanifires

def unify(qs):
    mask = [False]*len(qs)
    for i in range(len(qs)-1):
        if qs[i] == "E" and qs[i+1] == "E":
            mask[i] = True
        elif qs[i] == "A" and qs[i+1] == "A":
            mask[i] = True
    return [qs[i] for i in range(len(qs)) if not mask[i]]

def is_reducible_extend(qs1, qs2, graph):
    # 量化子列から共通の列を除いたものの関係をすでに知っていれば還元可能:TODO
    return False
def is_reducible_E8(qs1, qs2):
    # E8をAEに書き換えたものは還元可能:TODO
    return False
def is_reducible_A8(qs1, qs2):
    # A8をEAに書き換えたものは還元可能:TODO
    return False
def is_reducible_EEAA(qs1, qs2):
    # 重複するAやEを削除したものが同じなら還元可能
    return unify(qs1) == unify(qs2)

def is_reducible_redundant(qs1, qs2):
    #量化子列は冗長な量化子をつけたものに還元可能
    j = 0
    for i in range(len(qs1)):
        if j < len(qs2) and qs1[i] == qs2[j]:
            j += 1
    return j == len(qs2)

def is_reducible(qs1, qs2, graph):
    # qs1 <=m qs2
    return is_reducible_E8(qs1, qs2) \
        or is_reducible_A8(qs1, qs2) \
        or is_reducible_EEAA(qs1, qs2) \
        or is_reducible_redundant(qs1, qs2)\
        or is_reducible_extend(qs1, qs2, graph)

# def qs_to_id(qs):
#     id = 0
#     for i in range(len(qs)):
#         id *= 5
#         if qs[i] == "E":
#             id += 1
#         elif qs[i] == "A":
#             id += 2
#         elif qs[i] == "E8":
#             id += 3
#         elif qs[i] == "A8":
#             id += 4
#     return id


def generate_graph(n, clas):
    Graph = nx.DiGraph()
    nodes = generate_qutantifire(n, clas)
    for i in nodes:
        Graph.add_node( "." + "".join(i))
        Graph

    for v in itertools.permutations(nodes, 2):
        if is_reducible(v[0], v[1], Graph):
            Graph.add_edge( "." + "".join(v[0]), "." + "".join(v[1]))
            # Graph.add_edge(qs_to_id(v[0]), qs_to_id(v[1]))
    return Graph

if __name__ == "__main__":
    # sigma3 = generate_qutantifire(3, "sigma")
    graph = generate_graph(2, "sigma")
    # graph = nx.DiGraph([(1,2),(1,3),(2,4),(2,5),(3,6)])
    sccs = list(nx.strongly_connected_components(graph))
    cg = nx.condensation(graph, sccs) 
    names = {}
    for node in cg.nodes:
        names[node] = ", ".join(sccs[node])
    print(names)
    cg = nx.relabel_nodes(cg, names)
    g = nx.nx_agraph.to_agraph(cg)
    g.draw('sigma3-c.png',prog='dot')
    # g.write_pdf('sigma3-c.pdf')

