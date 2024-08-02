from collections import deque
import networkx as nx
import itertools
import json
import time
import sys
import functools
# import pydot



def quantifier_to_latex(q):
    match q:
        case 'E':
            return r"E"
        case 'A':
            return r"A"
        case 'E8':
            return r"E^{\infty}"
        case 'A8':
            return r"A^{\infty}"

class Quantifier:
    def __init__(self, base_list):
        self.base_list = base_list
        self.string_rep = qs_to_str(self.base_list)
        self.unified = None
        self.hash = hash(self.string_rep)
    def __str__(self) -> str:
        if self.base_list == []:
            return "C"
        else:
            return "$" + "".join(map(quantifier_to_latex,self.base_list)) + "$"
    def __repr__(self) -> str:
        return self.string_rep
    def __hash__(self) -> int:
        return self.hash
    def __eq__(self, other):
        if type(other) is type(self):
            return self.string_rep == other.string_rep
        else:
            return False
    def replace_E8(self):
        return Quantifier(replace_E8(self.base_list))
    def replace_A8(self):
        return Quantifier(replace_A8(self.base_list))
    def classify(self):
        return (self.type() , str(self.level()))
    def level(self):
        return level(self.base_list)
    def type(self):
        match repr(self.replace_A8().replace_E8())[0]:
            case "C":
                return "C"
            case "E":
                return "S"
            case "A":
                return "P"
    def unify(self):
        if self.unified is None:
            self.unified = unify(self.base_list)
        return self.unified
    def from_str(string: str):
        base_list = []
        for i in range(len(string)):
            match string[i]:
                case "E":
                    base_list.append("E")
                case "A":
                    base_list.append("A")
                case "8":
                    base_list[-1] += "8"
                case _:
                    raise ValueError("Invalid quantifier string " + string)
        return Quantifier(base_list)
        
    


# 量化子の列:(E, A, E8, A8)からなる配列

#TODO: Make quantifier type as a subclass of list, make it hashable, and move to set
def quantifier_extension_init_sigma(qs, n):
    return [(qs+["E"], 1), (qs+["E","E"], 1), (qs+["A8"], 2)]
def quantifier_extension_init_pi(qs, n):
    return [(qs+["A"], 1), (qs+["A","A"], 1), (qs+["A8"], 2)]
def quantifier_extension_init(qs,n):
    return [(qs+["E"], 1), (qs+["E","E"], 1), (qs+["E8"], 2),(qs+["A"], 1), (qs+["A","A"], 1), (qs+["A8"], 2)]
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

def quantifier_extension(qs, n):
    if qs == []:
        return quantifier_extension_init(qs, n)
    if qs[-1] == "E":
        return quantifier_extension_E(qs, n)
    elif qs[-1] == "A":
        return quantifier_extension_A(qs, n)
    elif qs[-1] == "E8":
        return quantifier_extension_E8(qs, n)
    elif qs[-1] == "A8":
        return quantifier_extension_A8(qs, n)
    
def generate_quantifier(n):
    quantifiers = []
    q = deque()
    q.append(([], 0)) #computable ralationから始める
    while len(q) > 0:
        qs, m = q.popleft()
        if m <= n:
            quantifiers.append(qs)  # class n以下なら量化子列を枚挙
            q.extend(quantifier_extension(qs, m)) # 後ろにくっつけて延長した量化子列を生成
    return quantifiers


def unify(qs):
    mask = [False]*len(qs)
    for i in range(len(qs)-1):
        if qs[i] == "E" and qs[i+1] == "E":
            mask[i] = True
        elif qs[i] == "A" and qs[i+1] == "A":
            mask[i] = True
    return [qs[i] for i in range(len(qs)) if not mask[i]]


def replace_E8(qs):
    return list(itertools.chain.from_iterable(map(lambda x : ["A", "E"] if x == "E8" else [x], qs)))

def replace_A8(qs):
    return list(itertools.chain.from_iterable(map(lambda x : ["E", "A"] if x == "A8" else [x], qs)))

def level(qs):
    return len(unify(replace_E8(replace_A8(qs))))

# @functools.cache
def remove_common_prefix(qs1, qs2):
    qs1l, qs2l = qs1.base_list, qs2.base_list
    shortest = min(len(qs1l), len(qs2l))
    index = 0
    zipped = itertools.zip_longest(qs1l, qs2l, fillvalue=None)
    no_common_prefix = list(itertools.dropwhile(lambda x : x[0] == x[1], zipped))
    new_qs1, new_qs2 = [x[0] for x in no_common_prefix if x[0] is not None], [x[1] for x in no_common_prefix if x[1] is not None]
    return Quantifier(new_qs2) ,Quantifier(new_qs1)

def is_reducible_extend(qs1, qs2, rels,debug=False):
    new_qs1, new_qs2 = remove_common_prefix(qs1, qs2)
    return new_qs2 in rels[new_qs1]

# @functools.cache
def is_reducible_E8(qs1, qs2):
    # return qs1.replace_E8() == qs2
    return replace_E8(qs1.base_list) == qs2.base_list
# @functools.cache
def is_reducible_A8(qs1, qs2):
    # return qs1.replace_A8() == qs2
    return replace_A8(qs1.base_list) == qs2.base_list
# @functools.cache
def is_reducible_EEAA(qs1, qs2):
    # 重複するAやEを削除したものが同じなら還元可能
    return qs1.unify() == qs2.unify()
    # return unify(qs1.base_list) == unify(qs2.base_list)
# @functools.cache
def is_reducible_redundant(qs1, qs2):
    #量化子列は冗長な量化子をつけたものに還元可能
    qs1l,  qs2l = qs1.base_list, qs2.base_list
    if qs1l == []:
        return True
    if qs2l == []:
        return False
    i1, i2 = iter(qs1l), iter(qs2l)
    n1, n2 = next(i1), next(i2)
    while True:
        if n1 == n2:
            try:
                n1 = next(i1)
            except:
                return True
        try:
            n2 = next(i2)
        except:
            return False
# @functools.cache     
def is_reducible_known(qs1, qs2):
    # EAE <=m A8E
    
    return (qs1, qs2) in known_relations
# @functools.cache
def is_reducible_lift(qs1: Quantifier, qs2: Quantifier, debug=False):
    if debug: print(qs1.base_list, qs2.base_list)
    if(len(qs1.base_list) < 1 or len(qs2.base_list) < 1):
        return False
    if qs1.base_list[0] == "A":
        if qs2.base_list[0] == "E8" or qs2.base_list[0] == "A8":
            return qs1.base_list[1:] == qs2.base_list[1:]
    if qs1.base_list[0] == "E":
        if qs2.base_list[0] == "E8":
            return qs1.base_list[1:] == qs2.base_list[1:]
    return False

def is_reducible(qs1 :Quantifier, qs2:Quantifier, rels:set[tuple[Quantifier,Quantifier]]):
    return is_reducible_known(qs1, qs2) \
        or is_reducible_E8(qs1, qs2) \
        or is_reducible_A8(qs1, qs2) \
        or is_reducible_lift(qs1, qs2) \
        or is_reducible_EEAA(qs1, qs2) \
        or is_reducible_redundant(qs1, qs2)\
        or is_reducible_extend(qs1, qs2, rels)\
        

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
    
def add_relations(nodes, rels: dict[Quantifier, set[Quantifier]] ):
    start = time.time()
    flag = False
    for (qs1, qs2) in itertools.permutations(nodes, 2):
        if qs2 in rels[qs1]:
            pass
        elif is_reducible(qs1, qs2, rels):
            rels[qs1].add(qs2)
            if not flag:
                print("New relation from rules")
            flag = True
        
    print(f"{time.time() - start:.3f}s to compute relations")
    return flag
    
# def closure_node(p, rels):
#     visited = {p}
#     children = set(rels[p].copy())
#     while len(children) > 0:
#         child = children.pop()
#         if child not in visited:
#             if child not in rels[p]:
#                 if not flag:
#                     print("New relation from closure")
#                 flag = True
#                 rels[p].add(child)
#                 # new_rels.append((p,child))
#             visited.add(child)
#             # print(rels[child])
#             for node in rels[child].copy():
#                 # print(node)
#                 children.add(node)
    
def dfs_closure(nodes, rels: dict[Quantifier, set[Quantifier]] ):
    flag = False
    start = time.time()
    new_rels = []
    for p in nodes:
        # print(p)
        # print(p, rels[p])
        visited = {p}
        children = set(rels[p].copy())
        while len(children) > 0:
            child = children.pop()
            if child not in visited:
                if child not in rels[p]:
                    if not flag:
                        print("New relation from closure")
                    flag = True
                    rels[p].add(child)
                    # new_rels.append((p,child))
                visited.add(child)
                # print(rels[child])
                for node in rels[child].copy():
                    # print(node)
                    children.add(node)
    # print(f"new rels: {new_rels}")
    print(f"{time.time() - start:.3f}s to compute transitive closure")
    return flag
                

def generate_graph(n):
    nodes = [Quantifier(qs) for qs in generate_quantifier(n)]
    print(len(nodes))
    print(repr(nodes[10]))
    rels: dict[Quantifier, set[Quantifier]] = {node : set() for node in nodes}
    flag = True
    count = 1
    while flag:
        flag = False
        print(f"Pass #{count}")
        count += 1
        rel_added = add_relations(nodes,rels)
        flag = flag or rel_added
        closed = dfs_closure(nodes,rels)
        flag = flag or closed
                
    return nodes,rels
        
        
known_relations = {
                        # (Quantifier(["E"]), Quantifier(["E8"])),
                    #    (Quantifier(["A"]), Quantifier(["A8"])),
                    #    (Quantifier(["A"]), Quantifier(["E8"])),
                    #    (Quantifier(["E"]), Quantifier(["A8"])),
                       (Quantifier(["A","E"]), Quantifier(["E8"])), #Result from PI_2 classification
                    #    (Quantifier(["E", "A", "E"]), Quantifier(["E","A8", "E"])), #Proposition 53
                       (Quantifier(["E8","A8"]), Quantifier(["E8","A"])), # Proposition 55
                    #    (Quantifier(["A","A8","A"]), Quantifier(["E8","A8","A"])), #Proposition 56
                    #    (Quantifier(["A","A8"]), Quantifier(["E8","A8"])), #Proposition 57
                    #    (Quantifier(["A","E","A"]), Quantifier(["A","E8","A"])),# Diagram 3
                    #    (Quantifier(["A","E","A"]), Quantifier(["E8","E","A8"])),# Diagram 3
    }

if __name__ == "__main__":
    n = int(sys.argv[1])
    nodes, rels = generate_graph(n)
    ae8a = Quantifier.from_str("AE8A")
    aea = Quantifier.from_str("AEA")
    e8a = Quantifier.from_str("E8A")
    ea = Quantifier.from_str("EA")
    print(is_reducible(aea, ae8a, rels))
    print(is_reducible(ea, e8a,rels))
    print(is_reducible_lift(ea, e8a))

    nodes = [node.base_list for node in nodes]
    rels_out = []
    for p,qs in rels.items():
        for q in qs:
            rels_out.append((p.base_list, q.base_list))
    with open("output.json", "w") as f:
        json.dump((nodes, rels_out), f)
    

