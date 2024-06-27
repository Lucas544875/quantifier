from collections import deque
import networkx as nx
import itertools
# import pydot

# 量化子の列:(E, A, E8, A8)からなる配列

def quantifier_extension_init_sigma(qs, n):
    return [(qs+["E"], 1), (qs+["E","E"], 1), (qs+["A8"], 2)]
def quantifier_extension_init_pi(qs, n):
    return [(qs+["A"], 1), (qs+["A","A"], 1), (qs+["A8"], 2)]

def quantifier_extension_E(qs, n):
    return [(qs+["A"], n+1), (qs+["A","A"], n+1), (qs+["A8"], n+1), (qs+["E8"], n+2)]
def quantifier_extension_A(qs, n):
    return [(qs+["E"], n+1),(qs+["E","E"], n+1), (qs+["E8"], n+1), (qs+["A8"], n+2)]
def quantifier_extension_E8(qs, n):
    return [(qs+["A"], n+1), (qs+["E"], n), (qs+["E","E"], n), (qs+["A8"], n+1), (qs+["E8"], n+2)]
    # return [(qs+["A"], n+1), (qs+["E"], n), (qs+["A8"], n+1), (qs+["E8"], n+2)]
def quantifier_extension_A8(qs, n):
    return [(qs+["E"], n+1), (qs+["A"], n), (qs+["A","A"], n), (qs+["E8"], n+1), (qs+["A8"], n+2)]
    # return [(qs+["E"], n+1), (qs+["A"], n), (qs+["E8"], n+1), (qs+["A8"], n+2)]

def quantifier_extension(qs, n, clas):
    if qs == []:
        if clas == "sigma":
            return quantifier_extension_init_sigma(qs, n)
        elif clas == "pi":
            return quantifier_extension_init_pi(qs, n)
    if qs[-1] == "E":
        return quantifier_extension_E(qs, n)
    elif qs[-1] == "A":
        return quantifier_extension_A(qs, n)
    elif qs[-1] == "E8":
        return quantifier_extension_E8(qs, n)
    elif qs[-1] == "A8":
        return quantifier_extension_A8(qs, n)
    
def generate_quantifier(n, clas):
    quantifiers = []
    q = deque()
    q.append(([], 0)) #computable ralationから始める
    while len(q) > 0:
        qs, m = q.popleft()
        if m <= n:
            quantifiers.append(qs)  # class n以下なら量化子列を枚挙
            q.extend(quantifier_extension(qs, m, clas)) # 後ろにくっつけて延長した量化子列を生成
    return quantifiers

def unify(qs):
    mask = [False]*len(qs)
    for i in range(len(qs)-1):
        if qs[i] == "E" and qs[i+1] == "E":
            mask[i] = True
        elif qs[i] == "A" and qs[i+1] == "A":
            mask[i] = True
    return [qs[i] for i in range(len(qs)) if not mask[i]]

def is_reducible_extend(qs1, qs2, rels):
    zipped = itertools.zip_longest(qs1, qs2, fillvalue=None)
    no_common_prefix = list(itertools.dropwhile(lambda x : x[0] == x[1], zipped))
    new_qs1, new_qs2 = [x[0] for x in no_common_prefix if x[0] is not None], [x[1] for x in no_common_prefix if x[1] is not None]
    return (new_qs1, new_qs2) in rels
def is_reducible_E8(qs1, qs2):
    new_qs1 = list(itertools.chain.from_iterable(map(lambda x : ["A", "E"] if x == "E8" else [x], qs1)))
    return new_qs1 == qs2
def is_reducible_A8(qs1, qs2):
    new_qs1 = list(itertools.chain.from_iterable(map(lambda x : ["E", "A"] if x == "A8" else [x], qs1)))
    return new_qs1 == qs2
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

def is_reducible(qs1, qs2, rels):
    # qs1 <=m qs2
    return is_reducible_E8(qs1, qs2) \
        or is_reducible_A8(qs1, qs2) \
        or is_reducible_EEAA(qs1, qs2) \
        or is_reducible_redundant(qs1, qs2)\
        or is_reducible_extend(qs1, qs2, rels)

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

def qs_to_str(qs):
    if qs == []:
        return "C"
    else:
        return "".join(qs)

def generate_graph(n, clas):
    nodes = generate_quantifier(n, clas)
    print(nodes)
    rels = []
    for (qs1, qs2) in itertools.permutations(nodes, 2):
        if is_reducible(qs1, qs2, rels):
            rels.append((qs1, qs2))
    return nodes,rels

def graph_from_nodes_rels(nodes,rels):
    Graph = nx.DiGraph()
    for node in nodes:
        Graph.add_node(qs_to_str(node))
    for (qs1, qs2) in rels:
        Graph.add_edge(qs_to_str(qs1), qs_to_str(qs2))
    return Graph
        

if __name__ == "__main__":
    graph = graph_from_nodes_rels(*generate_graph(2, "sigma"))
    output = ""
    for edge in graph.edges:
        output += edge[0] + " " + edge[1] + "\n"
    f = open("output.txt", "w")
    f.write(output)
    f.close()

