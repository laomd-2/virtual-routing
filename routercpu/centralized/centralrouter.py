from routercpu.centralized.controller import Controller
from routercpu.routable import Routable


class CentralRouter(Routable):

    def start(self):
        super().start()
        self.controller.addNeighbor(self.url)

    @property
    def controller(self):
        return self.getProxy("http://" + Controller.ip() + ":" + str(Controller.port()))

    def getNextHop(self, dst_url):
        return self.controller.getNext(self.url, dst_url)

    def addNeighbor(self, url, weight):
        super().addNeighbor(url, weight)
        self.controller.addEdges([(self.url, url, weight)])


import threading
if __name__ == '__main__':
    router = CentralRouter()
    t = threading.Thread(target=router.serve_forever)
    t.setDaemon(True)
    t.start()
    while not router.started:
        pass
    prefix = router.getIp()
    router.addNeighbor("http://" + prefix + ":12886", 4)
    # router.addNeighbor("http://" + prefix + ":12659", 1)
    # router.addNeighbor("http://" + prefix + ":12650", 0.5)
    while True:
        port = input("port: ")
        print(router.getNextHop("http://" + prefix + ":" + port))