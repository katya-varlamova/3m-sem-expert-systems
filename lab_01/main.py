from graphBFS import GraphBFS
from graphDFS import GraphDFS
from items import Edge, Node
import networkx as nx
import matplotlib.pyplot as plt
def show(arr: list):
    if arr == None:
        print("Not found")
        return
    for i in range(len(arr) - 1, -1, -1):
        if i != 0:
            print(f'{arr[i]} -> ', end='')
        else:
            print(f'{arr[i]}')


class Example:
    def edgeLst_1(self):
        G = nx.DiGraph()
        edgeLst = [
            Edge(Node(1), Node(2), 101),
            Edge(Node(1), Node(3), 102),
            Edge(Node(1), Node(4), 103),
            Edge(Node(2), Node(5), 104),
            Edge(Node(3), Node(4), 105),
            Edge(Node(4), Node(6), 106)
        ]
        for node in range(1, 7):
            G.add_node(str(node))
        for edge in edgeLst:
            G.add_edge(str(edge.get_start()), str(edge.get_end()))
        nx.draw(G, with_labels = True)
        plt.savefig("graph1.png")
        return edgeLst

    def edgeLst_2(self):
        G = nx.DiGraph()
        edgeLst = [
            Edge(Node(0), Node(1), 101),
            Edge(Node(0), Node(2), 102),
            Edge(Node(0), Node(3), 103),
            Edge(Node(1), Node(4), 104),
            Edge(Node(2), Node(4), 105),
            Edge(Node(2), Node(5), 106),
            Edge(Node(3), Node(5), 107),
            Edge(Node(3), Node(6), 108),
            Edge(Node(4), Node(8), 109),
            Edge(Node(5), Node(4), 110),
            Edge(Node(5), Node(7), 112),
            Edge(Node(5), Node(9), 111),
            Edge(Node(6), Node(7), 113),
            Edge(Node(7), Node(9), 115),
            Edge(Node(9), Node(8), 114)
        ]
        for node in range(0, 9):
            G.add_node(str(node))
        for edge in edgeLst:
            G.add_edge(str(edge.get_start()), str(edge.get_end()), weight = edge.get_label())
        
        nx.draw(G, with_labels = True)
        plt.savefig("graph2.png")
        plt.clf()
        return edgeLst


if __name__ == "__main__":
    print("Search methods in state graphs")

    print("Depth First Search")
    edgeLst = Example().edgeLst_2()
    res = GraphDFS(edgeLst).DFS(0, 7) # 2 1
    if res == None:
        print("Not found")
    else:
        res.show()

    print("-------------------------")

    print("Breadth First Search")
    edgeLst = Example().edgeLst_2()
    res = GraphBFS(edgeLst).BFS(0, 7)
    show(res)
