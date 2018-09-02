from routercpu.graphrouterbase import GraphRouterBase


class LSRouter(GraphRouterBase):

    def __init__(self):
        super().__init__()
        self.register_function(self.dfs)

    def dfs(self, data, tag, visited):
        visited[self.url] = True
        # print("recv", data, tag, ", sending to my neighbors")
        self.recv(data, tag)
        for url in self.neighbors:
            if url not in visited:
                try:
                    s = self.getProxy(url)
                    # print("sending to", url)
                    visited.update(s.dfs(data, tag, visited))
                    # print("done")
                    # print(visited)
                except OSError:
                    pass
        # print("end sended", visited)
        return visited

    def addNeighbor(self, url, weight):
        super().addNeighbor(url, weight)
        if not self.neighbors:
            try:
                s = self.getProxy(url)
                self.recv(s.send(), 'e')
            except OSError:
                pass
        self.dfs([(self.url, url, weight)], 'e', dict())

    def removeNeighbor(self, downs):
        super().removeNeighbor(downs)
        self.dfs(downs, 'd', dict())


import threading
if __name__ == '__main__':
    router = LSRouter()
    t = threading.Thread(target=router.serve_forever)
    t.setDaemon(True)
    t.start()
    while not router.started:
        pass
    router.addNeighbor("http://172.19.103.202:12564", 4)
    router.addNeighbor("http://172.19.103.202:12659", 1)
    router.addNeighbor("http://172.19.103.202:12650", 0.5)
    while True:
        port = input("port: ")
        print(router.getNextHop("http://172.19.103.202:" + port))