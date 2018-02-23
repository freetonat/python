#! /usr/bin/env python
__author__ ='eyonson'
__version__ = '1.0'
import sys
#sys.path.insert(0, '/home/eyonson/CLI_R5A42/src')
sys.path.insert(0, '/home/eyonson/CLI_R5A42/src_no_output')
import time, datetime
import re
import autott.session
import StringIO
import os

import logging.handlers

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s > %(message)s')

filehandler = logging.FileHandler('./sgw_reload_test.log')
streamHandler = logging.StreamHandler()

filehandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(filehandler)
logger.addHandler(streamHandler)

class pgw_peer_cli():
    def __init__(self, target):
        self.target = target
        self.node = autott.session.SSRNode(self.target)

    def peer_cnt(self):
        oam_cli = self.node.oam_cli
        output = oam_cli.do('ManagedElement=1,Epg=1,Pgw=1,statistics dbpPeer')
        lines = StringIO.StringIO(output)
        for line in lines:
            mat = (re.search(r'sgw-nbr-of-bearers', line))
            if mat:
                print(line)

    def update_peer_info(self):
        """Update and return node status info."""
        logger.info("Updating node status info")
        oam_cli = self.node.oam_cli
        output = oam_cli.do('ManagedElement=1,Epg=1,Pgw=1,statistics dbpPeer')

        if output.count("not available"):
            print("The node service is unavailable")
            self.status_info = ""
            return False
        elif output.count("peer:"):
            self.update_peer_status(output)



        else:
            print("Unknown service")
            return False

    def _add_peer(self, peername):
        if not self.peer_dics.has_key(peername):
            peer_inst = PEERList()
            self.peer_dics[peername] = peer_inst
        return self.peer_dics[peername]

    def update_peer_status(self, peer_str):
        """Update pic status."""
        self.peer_dics = {}
        peername = None
        for line in StringIO.StringIO(peer_str):
            line = line.strip()

            mat = re.match(r'\s*name:\s*(\S*)', line, re.I)
            if mat:
                peername = mat.group(1)
                pic = self._add_peer(peername)
                continue

            if not self.peer_dics.get(peername, None):
                continue

            mat = re.match(r's*initial-send-success:\s*(\d*)', line, re.I)
            if mat:
                self.peer_dics[peername].initial_send_success = mat.group(1)
                continue

            mat = re.match(r's*initial-send-failed-policing:\s*(\d*)', line, re.I)
            if mat:
                self.peer_dics[peername].initial_send_success = mat.group(1)
                continue

            mat = re.match(r's*update-send-success:\s*(\d*)', line, re.I)
            if mat:
                self.peer_dics[peername].initial_send_success = mat.group(1)
                continue

            mat = re.match(r's*update-send-failed-policing:\s*(\d*)', line, re.I)
            if mat:
                self.peer_dics[peername].initial_send_success = mat.group(1)
                continue   

class PEERList(object):
    def __init__(self):
        self.initial_send_success = 0
        self.initial_send_failed_policing = 0
        self.update_send_success = 0
        self.update_send_failed_policing = 0

if __name__ == '__main__':
    target = str(sys.argv[1])  # target is epgx-x
    peer_cnt = pgw_peer_cli(target)
    peer_cnt.update_peer_info()