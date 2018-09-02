from cmd import Cmd
from routeserver import RouteServer
from threading import Thread
from xmlrpc.client import Binary


class Terminal(Cmd):
    """docstring for Terminal"""

    def __init__(self):
        Cmd.__init__(self)
        self.n = RouteServer()

        # 服务器, 自动将输入队列的内容传到输出队列内容, 自动将输出队列中的内容传输出去
        targets = [self.n.start, self.n.checkInputQue, self.n.checkOutque]
        for target in targets:
            t = Thread(target=target)
            t.setDaemon(True)
            t.start()

        self.name_dic = {'A': '172.19.123.243', 'B': '192.168.155.4',
                         'C': '192.168.155.3', 'D': '192.168.155.2'}

    def do_sendMes(self, host_name):
        if host_name not in self.name_dic:
            print("host name invalid")
            return
        message = input("mes:")
        package = {"des_ip": self.name_dic[
            host_name], "data": message, 'isMes': 1}
        self.n.addQue(package)

    def do_sendFile(self, host_name):
        if host_name not in self.name_dic:
            print("host name invalid")
            return
        handle = open("1.mp4", 'rb')
        content = Binary(handle.read())
        package = {"des_ip": self.name_dic[
            host_name], "data": content, 'isMes': 0}
        self.n.addQue(package)


if __name__ == '__main__':
    client = Terminal()
    client.cmdloop()
