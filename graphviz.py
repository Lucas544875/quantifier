import networkx as nx
import random
from networkx.drawing.nx_agraph import graphviz_layout
random.seed(0) # seed値を0に固定
G = nx.DiGraph([(1,2),(1,3),(2,4),(2,5),(3,6)]) # 1から2，1から3へのエッジとなるような有向グラフの作成
pos = graphviz_layout(G,prog="dot") # 描画レイアウトの指定 Graphvizの"dot"というレイアウトを使用
nx.draw(G,pos=pos,with_labels=True) # pos=posでGraphvizのレイアウト通りのグラフを描画
