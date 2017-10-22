# -*- coding: utf-8 -*-
"""
模块说明：蓝牙连接器

"""

import threading
import time
import logging

class BtConnector:
    def __init__(self):
        self._running = True
        logging.basicConfig(filename='mothership.log',level=logging.DEBUG)
        self.rcvinfo = None

    def start(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self,sock, info):
        while self._running:
            try:
                #接收1024个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
                receive=sock.recv(1024).decode('utf-8');
                self.rcvinfo=receive
                #打印刚刚读到的东西(info=地址)
                print('['+str(info)+']'+receive);
                logging.debug("received: %s", receive)
                #回传数据给发送者
                sock.send("ok".encode('utf-8'));
            except Exception as e:
                logging.warning("exception: %s", e)
                logging.info("connection released")
                print("connection released")
                self.terminate()

    def get_rcvinfo(self):
        return self.rcvinfo