import networkx as nx
import random
from networkx.drawing.nx_agraph import graphviz_layout
import pygraphviz as pgv

random.seed(0) # seed値を0に固定
G = nx.DiGraph([(1,2),(1,3),(2,4),(2,5),(3,6)]) # 1から2，1から3へのエッジとなるような有向グラフの作成
# g = nx.to_agraph(G)
g = nx.nx_agraph.to_agraph(G)
g.draw('test.png',prog='dot')