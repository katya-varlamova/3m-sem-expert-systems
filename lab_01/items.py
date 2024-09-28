class Node:
    def __init__(self, number: int):
        self.number = number

    def __str__(self):
        res = '' + f'{self.number}'
        return res

    def __repr__(self):
        res = '' + f'{self.number}'
        return res


class Edge:
    def __init__(self, startNode: Node, endNode: Node, label):
        self.startNode = startNode
        self.endNode = endNode
        self.label = label
        self.used = False
    def get_start(self):
        return self.startNode
    def get_end(self):
        return self.endNode

    def get_label(self):
        return self.label
