from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy
import socket, urllib.parse, random


class Routable(SimpleXMLRPCServer):

    def __init__(self):
        self.url = "http://" + self.getIp() + ':' + str(self.port())
        super().__init__(("", self.getPort(self.url)), logRequests=False)
        self.register_function(self.testProxy)
        self.started = False

    @staticmethod
    def port():
        return 13000

    def start(self):
        print(self.url,
              "succeeded to start up!")
        self.started = True

    def service_actions(self):
        super().service_actions()
        if not self.started:
            self.start()

    def getProxy(self, url):
        return ServerProxy(url, use_builtin_types=True)

    def testProxy(self, op):
        return op

    def addNeighbor(self, url, weight):
        pass

    def getNextHop(self, dst_url):
        pass

    @staticmethod
    def getIp():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            return s.getsockname()[0]
        except OSError:
            print("网络连接失败")
        finally:
            s.close()

    @staticmethod
    def getPort(url):
        return int(urllib.parse.urlparse(url)[1].split(':')[-1])

