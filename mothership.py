# -*- coding: utf-8 -*-
"""
模块说明：主程序启动模块

"""
import bluetooth
import threading
import logging
import BtConnector
import BaseHTTPServer
import SocketServer

def runbc(server_socket, bc):
    #等待有人来连接,如果没人来,就阻塞线程等待(这本来要搞个会话池,以方便给不同的设备发送数据)
    sock,info=server_socket.accept();
    #打印有人来了的消息
    print(str(info[0])+' Connected!');
    logging.info(str(info[0])+' Connected!')
    #创建一个线程专门服务新来的连接(这本来应该搞个线程池来管理线程的)
    bc.start()
    t=threading.Thread(target=bc.run,args=(sock,info[0]))
    #设置线程守护,防止程序在线程结束前结束
    t.setDaemon(True)
    #启动线程
    t.start();

def runhttpd(port, bc):
    class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bc.get_rcvinfo())
    #httpd = SocketServer.TCPServer(("127.0.0.1",port), MyHandler)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(("127.0.0.1", port), MyHandler)
    try:
        logging.debug("starting httpd server on port %d", port)
        httpd.serve_forever()
    except Exception as e:
        logging.error(e)
        pass
    httpd.server_close()

if __name__ == '__main__':
    #主线程
    #创建一个服务器套接字,用来监听端口
    server_socket=bluetooth.BluetoothSocket(bluetooth.RFCOMM);
    #允许任何地址的主机连接,未知参数:1(端口号,通道号)
    server_socket.bind(("",1))
    #监听端口/通道
    server_socket.listen(1);
    bc = BtConnector.BtConnector()
    logging.basicConfig(filename='mothership.log',level=logging.DEBUG)
    threads = []

    #开死循环 等待客户端连接
    bt=threading.Thread(target=runbc, args=(server_socket, bc))
    threads.append(bt)
    bt.setDaemon(True)

    port = 7600
    ht=threading.Thread(target=runhttpd, args=(port,bc))
    threads.append(ht)
    bt.setDaemon(True)

    for t in threads:
        t.start();
        t.join();


