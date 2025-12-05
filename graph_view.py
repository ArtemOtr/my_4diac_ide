import networkx as nx
import matplotlib.pyplot as plt

class FBGraphView:
    def __init__(self, blocks, ev_conns, data_conns):
        self.blocks = blocks
        self.ev = ev_conns
        self.data = data_conns

    def show(self):
        G = nx.DiGraph()

        for b in self.blocks:
            G.add_node(b["name"])

        for s, d in self.ev:
            G.add_edge(s.split(".")[0], d.split(".")[0])

        for s, d in self.data:
            G.add_edge(s.split(".")[0], d.split(".")[0])

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color="lightblue")
        plt.title("FB Network")
        plt.show()
