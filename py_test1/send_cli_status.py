#! /usr/bin/env python
__author__ ='eyonson'
__version__ = '1.0'
import sys
import time
import re
import StringIO

class send_cli():

    def __init__(self, target):
        self.target = target

    def update_status_info(self):
        """Update and return node status info."""
        print("Updating node status info")
        f = open("status.txt", "r")
        output = f.read()

        if output.count("not available"):
            print("The node service is unavailable")
            self.status_info = ""
            return False
        elif output.count("board-information:"):
            self.status_info = output
            self.update_board_status(output)
            sgw_rest = self.getlist_sgwbearers()
            pgw_rest = self.getlist_pgwbearers()
            sgw_uplink_packet = self.getlist_uplink_packet()
            sgw_downlink_packet = self.getlist_downlink_packet()
            print("SGW session cnt      = {}, SGW pkt session cnt = {}".format(sgw_rest,pgw_rest))
            print("SGW session cnt sum  = {}, SGW session cnt sum = {}".format(sum(sgw_rest),sum(pgw_rest)))
            print("SGW uplink packet cnt = {}, SGW downlink packet cnt = {}".format(sgw_uplink_packet, sgw_downlink_packet))
            print("SGW uplink packet sum = {}, SGW downlink packet sum = {}".format(sum(sgw_uplink_packet),sum(sgw_downlink_packet)))
            if (sum(sgw_rest) != sum(pgw_rest)) :
                print('##### Happen #####')

            return self.status_info
        else:
            print("Unknown service")
            self.status_info = ""
            return False

    def getlist_sgwbearers(self):
        sgw_bearers_list = []
        for pic_name in self.board_dics.keys():
            print("pic_name = {}".format(pic_name))
            pic = self.board_dics[pic_name]
            sgw_bearers = pic.sgw_number_bearers
            sgw_bearers_list.append(sgw_bearers)
        return sgw_bearers_list

    def getlist_pgwbearers(self):
        pgw_bearers_list = []
        for pic_name in self.board_dics.keys():
            pic = self.board_dics[pic_name]
            pgw_bearers = pic.pgw_number_bearers
            pgw_bearers_list.append(pgw_bearers)
        return pgw_bearers_list

    def _add_board(self, itfname):
        if not self.board_dics.has_key(itfname):
            board_inst = SSRBoard()
            self.board_dics[itfname] = board_inst
        return self.board_dics[itfname]

    def getlist_uplink_packet(self):
        sgw_uplink_list = []
        for pic_name in self.board_dics.keys():
            pic = self.board_dics[pic_name]
            uplink_packet = pic.uplink_packets
            sgw_uplink_list.append(uplink_packet)
        return sgw_uplink_list

    def getlist_downlink_packet(self):
        sgw_downlink_list = []
        for pic_name in self.board_dics.keys():
            pic = self.board_dics[pic_name]
            downlink_packet = pic.downlink_packets
            sgw_downlink_list.append(downlink_packet)
        return sgw_downlink_list

    def update_board_status(self, status_str):
        """Update pic status."""

        self.board_dics = {}

        itfname = None
        board_fun = None
        for line in StringIO.StringIO(status_str):
            line = line.strip()

            mat = re.match(r'\s*board:\s*(\w+-\d+/\d+/\d+)', line, re.I)
            if mat:
                itfname = mat.group(1)
                pic = self._add_board(itfname)
                pic.srv_interface = itfname
                continue

            if not self.board_dics.get(itfname, None):
                continue

            mat = re.match(r'\s*internal-address:\s*(.+)', line, re.I)
            if mat:
                self.board_dics[itfname].internal_addr = mat.group(1)
                continue

            mat = re.match(r"\s*cpu-utilization:\s*Peak\s*(\d+)%, Average\s*(\d+)%", line, re.I)
            if mat:
                self.board_dics[itfname].cpu_peak_load = float(mat.group(1))
                self.board_dics[itfname].cpu_avg_load = float(mat.group(2))
                continue

            mat = re.match(r"\s*memory:\s*Total\s*(\d+), Used\s*(\d+)", line, re.I)
            if mat:
                self.board_dics[itfname].mem_total = float(mat.group(1))
                self.board_dics[itfname].mem_used = float(mat.group(2))
                continue

            mat = re.match(r'\s*function-name:\s*(.+)', line, re.I)
            if mat:
                board_fun = mat.group(1)
                print('function-name={}'.format(board_fun))
                if 'Spare' in board_fun:
                    self.board_dics[itfname].function.append(board_fun)
                continue

            mat = re.match(r'\s*status:\s*Ready', line, re.I)
            if mat:
                self.board_dics[itfname].function.append(board_fun)
                print('board_dics = {}'.format(self.board_dics[itfname]))

            mat = re.match(r'\s*status:\s*(not ready|standby)', line, re.I)
            if mat and board_fun.count("Secondary PGW Session Controller"):
                self.board_dics[itfname].function.append(board_fun)

            mat = re.match(r'\s*status:\s*Not ready', line, re.I)
            if mat and not board_fun.count("Secondary PGW Session Controller"):
                self.board_dics[itfname].not_ready.append((itfname, board_fun))
                continue

            mat = re.match(r'number-of-bearers:\s*(\d+)', line, re.I)
            if mat:
                if board_fun.count('SGW Session Controller'):
                    self.board_dics[itfname].sgw_number_bearers = int(mat.group(1))

                elif board_fun.count('SGW Packet Processor'):
                    self.board_dics[itfname].pgw_number_bearers = int(mat.group(1))

            mat = re.match(r'uplink-packets:\s*(\d+)', line, re.I)
            if mat:
                if board_fun.count('SGW Packet Processor'):
                    self.board_dics[itfname].uplink_packets = int(mat.group(1))

            mat = re.match(r'downlink-packets:\s*(\d+)', line, re.I)
            if mat:
                if board_fun.count('SGW Packet Processor'):
                    self.board_dics[itfname].downlink_packets = int(mat.group(1))

class Board(object):

    def __init__(self):
        self.function = []

    def is_pp(self):
        """Return True if the pic is a packet processor."""
        return self.function.count("Packet Processor") or self.function.count("MBMS-GW Packet Processor")

    def is_spp(self):
        """Return True if the pic is an sgw packet processor."""
        return self.function.count("SGW Packet Processor")

    def is_gsc(self):
        """Return True if the pic is a global session controller."""
        return self.function.count("Global Session Controller")

    def is_psc(self):
        """Return True if the pic is a pgw session controller."""
        return self.function.count("PGW Session Controller")

    def is_ssc(self):
        """Return True if the pic is a sgw session controller."""
        return self.function.count("SGW Session Controller")

    def is_spare(self):
        """Return True if the pic is spare."""
        return self.function.count("Spare")

    def is_secpsc(self):
        """Return True if the pic is secondary psc."""
        return self.function.count("Secondary PGW Session Controller")

    def is_ppp(self):
        """Return True if the pic is a pgw packet processor."""
        return self.function.count("PGW Packet Processor")

class SSRBoard(Board):

    """Store the SSR's board info."""

    def __init__(self):
        Board.__init__(self)
        self.srv_interface = '-'
        self.internal_addr = None
        self.hw_version = ''
        self.sw_version = ''
        self.cpu_peak_load = 0
        self.cpu_avg_load = 0
        self.mem_total = 0
        self.mem_used = 0
        self.sgw_number_bearers = 0
        self.pgw_number_bearers = 0
        self.not_ready = []
        self.uplink_packets = 0
        self.downlink_packets = 0

        # ssr specific
        self.board_idx = None

    def is_l2tpboard(self):
        """Return the board is sc or not."""

        return self.function.count("Packet Processor L2TP") or \
            self.function.count("L2TP Packet Processor")

sending_cli = send_cli('epg1-1')
sending_cli.update_status_info()


