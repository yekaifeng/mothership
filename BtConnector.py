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

    def terminate(self):
        self._running = False

    def run(self,sock, info):
        while self._running:
            try:
                #接收1024个字节,然后以UTF-8解码(中文),如果没有可以接收的信息则自动阻塞线程(API)
                receive=sock.recv(1024).decode('utf-8');
                #打印刚刚读到的东西(info=地址)
                print('['+str(info)+']'+receive);
                #为了返回好看点,加个换行
                receive=receive+"\n";
                #回传数据给发送者
                sock.send(receive.encode('utf-8'));
            except Exception as e:
                logging.warning("exception: %s", e)
                logging.info("connection released")
                print("connection released")
                self.terminate()

