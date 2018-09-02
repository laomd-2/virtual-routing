from routercpu.routerbase import RouterBase
from networkx.algorithms import dijkstra_path


class GraphRouterBase(RouterBase):

    def __init__(self):
        super().__init__()
        self.register_function(self.send)

    def start(self):
        super().start()
        self.recv(self.url, 'u')

    def addItem(self, dst_url):
        try:
            path = dijkstra_path(self._graph, self.url, dst_url)
            self._table[dst_url] = path[1] if len(path) > 1 else path[0]
        except Exception as e:
            print(e)

    def send(self):
        return [(u, v, self._graph.get_edge_data(u, v)['weight']) for u, v in self._graph.edges]

    def recv(self, data, tag):
        if tag == 'e':
            self._graph.add_weighted_edges_from(data)
        elif tag == 'u':
            self._graph.add_node(data)
        elif tag == 'd':
            for v in data:
                self._graph.remove_node(v)
            if self.url not in self._graph:
                self._graph.add_node(self.url)
        for url in self._table:
            self.addItem(url)
        # pprint.pprint(self._graph.nodes)
        # print("EdgeView", end='')
        # pprint.pprint(self.send())
        # pprint.pprint(self._table)

