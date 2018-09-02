
from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from routercpu.centralized.centralrouter import CentralRouter
# from routercpu.distributed.lsrouter import LSRouter
import queue, threading


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """多线程服务器类,可处理多个客户端连接服务器"""
    pass


class RouteServer(object):
    """路由器类"""

    def transport(self, package):
        """交换结构，把数据包从输入队列传到输出队列"""
        self.output_que.put(package)

    def buildGragh(self):
        self.routercpu = CentralRouter()
        t = threading.Thread(target=self.routercpu.serve_forever)
        t.setDaemon(True)
        t.start()
        while not self.routercpu.started:
            pass
        self.routercpu.addNeighbor("http://172.18.32.225:13000", 5)
        # self.routercpu.addNeighbor("http://192.168.155.2:13000", 1)

    def laomd(self, destination_ip):
        return self.routercpu.getNextHop("http://" + str(destination_ip) + ":13000")

    def checkOutque(self):
        """自动检测输出队列"""
        while True:
            while not self.output_que.empty():
                package = self.output_que.get()
                self.proxy.addQue(package)

    def addQue(self, content):
        self.input_que.put(content)

    def checkInputQue(self):
        while True:
            while not self.input_que.empty():
                package = self.input_que.get()
                localIp = self.routercpu.getIp()
                if package['des_ip'] == localIp:  # 如果目标ip就是本机ip，就把包拦截下来处理
                    if package['isMes'] == 0:
                        self.fetch_file(package['data'])
                    else:
                        self.show_message(package['data'])
                else:
                    des_ip = package["des_ip"]
                    next_ip = self.laomd(des_ip)
                    try:
                        self.proxy = ServerProxy(next_ip.replace("13000", "12001"))
                        self.transport(package)
                    except OSError as e:
                        print("Connection failed.", e)
                    except Exception as e:
                        print(e)

    def show_message(self, content):
        print(content)

    def fetch_file(self, content):
        handle = open("1.mp4", "wb")
        handle.write(content.data)
        handle.close()

    def start(self):
        self.buildGragh()
        svr = ThreadXMLRPCServer(("", 12001), allow_none=True)
        svr.register_function(self.addQue)  # 注册函数
        svr.register_function(self.fetch_file)
        svr.serve_forever()

    def __init__(self):

        self.input_que = queue.Queue(maxsize=10)
        self.output_que = queue.Queue(maxsize=10)
