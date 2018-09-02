from routercpu.routable import Routable
from networkx.classes.graph import Graph


class RouterBase(Routable):

    def __init__(self):
        super().__init__()
        self._table = {self.url: self.url}
        self._graph = Graph()

    def addItem(self, dst_url):
        pass

    def removeNeighbor(self, downs):
        for url in downs:
            if url in self._table:
                del self._table[url]

    def getNextHop(self, dst_url):
        downs = []
        for url in self.neighbors:
            try:
                s = self.getProxy(url)
                s.testProxy(0)
            except OSError:
                downs.append(url)
        if downs:
            self.removeNeighbor(downs)
        if dst_url not in self._table:
            self.addItem(dst_url)
        try:
            return self._table[dst_url]
        except KeyError:
            return ""

    @property
    def neighbors(self):
        if self.url not in self._graph:
            self._graph.add_node(self.url)
        return self._graph[self.url]

