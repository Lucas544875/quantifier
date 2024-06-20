from collections import deque
import networkx as nx
import itertools

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
    sigma3 = []
    q = deque()
    q.append(([], 0))
    while len(q) > 0:
        qs, m = q.popleft()
        if m <= n:
            sigma3.append(qs)
            q.extend(quantifire_extention(qs, m, clas))
    return sigma3
    
def is_reducible_extend(qs1, qs2, graph):
    # 量化子列から共通の列を除いたものの関係をすでに知っていれば還元可能
    pass
def is_reducible_E8(qs1, qs2):
    # E8をAEに書き換えたものは還元可能
    pass
def is_reducible_A8(qs1, qs2):
    # A8をEAに書き換えたものは還元可能
    pass
def is_reducible_EEAA(qs1, qs2):
    # 重複するAやEを削除したものに還元可能
    pass
def is_reducible_redundant(qs1, qs2):
    #量化子列は冗長な量化子をつけたものに還元可能
    pass

def is_reducible(qs1, qs2,graph):
    return is_reducible_E8(qs1, qs2) \
        or is_reducible_A8(qs1, qs2) \
        or is_reducible_EEAA(qs1, qs2) \
        or is_reducible_redundant(qs1, qs2)\
        or is_reducible_extend(qs1, qs2, graph)


def generate_graph(n, clas):
    Graph = nx.DiGraph()
    nodes = generate_qutantifire(n, clas)
    for i in nodes:
        Graph.add_node("".join(i))

    for v in itertools.permutations(nodes, 2):
        if is_reducible(v[0], v[1], Graph):
            Graph.add_edge("".join(v[0]), "".join(v[1]))

if __name__ == "__main__":
    sigma3 = generate_qutantifire(3, "sigma")
    graph = generate_graph(3, "sigma")
