from routercpu.graphrouterbase import GraphRouterBase
from networkx.classes.graph import Graph
import sys, pprint


class Controller(GraphRouterBase):

    def __init__(self):
        super().__init__()
        self._table.clear()
        self._all = Graph()
        self.register_function(self.addNeighbor)
        self.register_function(self.addEdges)
        self.register_function(self.getNext)

    def getNext(self, src, dst):
        self.url, src = src, self.url
        next_hop = self.getNextHop(dst)
        self.url, src = src, self.url
        pprint.pprint(self._table)
        return next_hop

    @staticmethod
    def port():
        return 12345

    @staticmethod
    def ip():
        return "172.19.123.243"

    def addNeighbor(self, url, weight=sys.maxsize):
        self.recv(url, 'u')
        self._graph, self._all = self._all, self._graph
        super().addNeighbor(url, weight)
        self.recv([(self.url, url, weight)], 'e')
        self._graph, self._all = self._all, self._graph
        return 0

    def addEdges(self, edges):
        self.recv(edges, 'e')
        return 0

    def removeNeighbor(self, downs):
        super().removeNeighbor(downs)
        self.recv(downs, 'd')


if __name__ == '__main__':
    ctrl = Controller()
    ctrl.serve_forever()