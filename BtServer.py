# -*- coding: utf-8 -*-
"""
模块说明：蓝牙串口服务器

"""
import logging

class BtServer:
    def __init__(self):
        self._running = True
        logging.basicConfig(filename='mothership.log',level=logging.DEBUG)

    def terminate(self):
        self._running = False

    def run(self,sock, info):
        while self._running:
            try:
                pass
            except Exception as e:
                logging.warning("exception: %s", e)
                self.terminate()