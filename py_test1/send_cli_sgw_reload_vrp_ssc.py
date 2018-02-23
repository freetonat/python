#! /usr/bin/env python
__author__ ='eyonson'
__version__ = '1.0'
import sys 
sys.path.insert(0, '/home/eyonson/CLI_R5A42/src')
import time
import re
import autott.session
import simtool.blade
import StringIO
import logging
import logging.handlers

logger = logging.getLogger("log")
logger.setLevel(logging.INFO)

#formatter = logging.Formatter('[%(levelname)s%:(filename)s:%(lineno)s]%(asctime)s > %(message)s')
formatter = logging.Formatter('%(asctime)s > %(message)s')

filehandler = logging.FileHandler('./sgw_reload_test.log')
streamHandler = logging.StreamHandler()

filehandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(filehandler)
logger.addHandler(streamHandler)

class testStart():

    def __init__(self, target):
        self.target = target
        self.stop_flag = False

    def do(self):
        boardmg = Board_manager(target)
        bearer_count = sgwBearerCnt_cli(target)
        origin_bearer_cnt = bearer_count.update_status_info()
        for i in range(1,5):        
            print
            logger.info("********************** START TEST No %d **********************" % i) 
            while True:
                ret = bearer_count.is_node_ready()
                if ret == True:
                    logger.info("### Board status is all ready")
                    print
                    break
                if ret == False:
                    logger.info("### Board status is not  ready")
                    time.sleep(10)
                    continue
            boardmg.reload_switchover("vrp")
            time.sleep(30)
            del boardmg
            del bearer_count

            boardmg = Board_manager(target)
            bearer_count = sgwBearerCnt_cli(target)

            boardmg.show_redundancy()
            time.sleep(5)
            boardmg._reload_card(3)
            time.sleep(60)
            boardmg.show_redundancy()
            time.sleep(5)
            while True:
                ret = bearer_count.is_node_ready()
                if ret == True:
                    logger.info("### Board status is all ready")
                    updated_bearer_cnt = bearer_count.update_status_info()
                    if origin_bearer_cnt != updated_bearer_cnt:
                        logger.info("########### Mismatch Bearer count ###################")
                        self.stop_flag = True
                        break
                    else:
                        logger.info("### Bearer count is same as origin")
                        break
                if ret == False:
                    logger.info("### Board status is not  ready")
                    time.sleep(10)
                    continue
            if self.stop_flag == True:
                break
            time.sleep(120)
            boardmg.show_redundancy()
            time.sleep(5)
            while True:
                ret = boardmg.check_redundancy()
                if ret == True:
                    logger.info("RIB redundancy SUCCESS")
                    break
                else:
                    logger.info("RIB redundancy Not ready")
                    time.sleep(20)
                    continue
            #bearer_count.sgw_bearer_cnt()
            #time.sleep(20)

class sgwBearerCnt_cli():

    def __init__(self, target):
        self.target = target
        self.node = autott.session.SSRNode(self.target)
        self.blade = 'epgtool'+self.target[3:]+'0'
        self.tool = simtool.blade.Blade(self.blade)

    def sgw_bearer_cnt(self):
        oam_cli = self.node.oam_cli
        output = oam_cli.do('ManagedElement=1,Epg=1,Sgw=1,statistics')
        lines = StringIO.StringIO(output)
        for  line in lines:
            mat = (re.search(r'sgw-nbr-of-bearers' , line))
            if mat:
                print(line)

    def update_status_info(self):
        """Update and return node status info."""
        logger.info("Updating node status info")
        oam_cli = self.node.oam_cli
        output = oam_cli.do('ManagedElement=1,Epg=1,Node=1,status')

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
            print
            logger.info("### SGW session cnt = {}, SGW pkt session cnt = {}".format(sgw_rest,pgw_rest))
            logger.info("### SGW session cnt sum = {}, SGW pkt session cnt sum = {}".format(sum(sgw_rest),sum(pgw_rest)))
            print("SGW uplink packet cnt = {}, SGW downlink packet cnt = {}".format(sgw_uplink_packet,sgw_downlink_packet))
            print("SGW uplink packet sum = {}, SGW downlink packet sum = {}".format(sum(sgw_uplink_packet),sum(sgw_downlink_packet)))
            print
            #if (sum(sgw_rest) != sum(pgw_rest)) :
		    #print('##### Happen #####')
    
            return sum(sgw_rest)
        else:
            print("Unknown service")
            self.status_info = ""
            return False

    def is_node_ready(self):
        oam_cli = self.node.oam_cli
        node_status = oam_cli.do('ManagedElement=1,Epg=1,Node=1,status')
        node_ready = False
        node_ready = not bool(node_status.count('status: ') - node_status.count('status: Ready') -
                              node_status.count(': Spare'))
        return node_ready

    def getlist_sgwbearers(self):
        sgw_bearers_list = []
        for pic_name in self.board_dics.keys():
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


class Board_manager():

    def __init__(self, target):
        self.target = target
        self._cards_status = {}
        self.node = autott.session.SSRNode(self.target)
        self.blade = 'epgtool'+self.target[3:]+'0'
        self.tool = simtool.blade.Blade(self.blade)

    def show_redundancy(self):
        output = self.node.erv_cli.do('show redundancy')
        for line in StringIO.StringIO(output):
            line = line.strip()
            if 'RIB          ' in line:
                print
                logger.info("### " + line) 
                print

    def check_redundancy(self):
        output = self.node.erv_cli.do('show redundancy')
        for line in StringIO.StringIO(output):
            line = line.strip()
            if 'RIB          ' in line:
                rib_status = re.split(':', line)[1]
                if rib_status == " SUCCESS":
                    return True
                else:
                    return False

    def _ssc_ready(self, cards=None):
        output = self.node.erv_cli.do('show chassis')
        results = re.findall(r'(\d+)\s+:\s+v?(ssc|srvc|vsfo).*?\s+.*?\s+(\w+)', output)
        if cards:
            ret = all([state == "IS" for n, _, state in results if n in cards])
        else:
            ret = len(results) == [x for _, _, x in results].count('IS')
        if not ret:
            print("one or more ssc cards were not in IS status")
        return ret


    def _reload_card(self, slot_num):
        """Reload card."""

        erv_cli = self.node.erv_cli
        logger.info("Doing the reload cards %s", slot_num)
        erv_cli.sendline("reload card %s" % slot_num)
        ret = erv_cli.expect(["want to reload"], timeout=60)
        print("Node info: %s", erv_cli.before)
        if ret == 0:
            erv_cli.do("y")
            print("Sending yes to really want to reload the card %s", slot_num)
        else:
            raise E.NodeError("Reload failed, got unknown response from node")

    def reload_switchover(self, switchover_type):
        """Reload standby."""

        erv_cli = self.node.erv_cli
        expect_list = ["configuration", "want to reload"]
        if switchover_type != "alsw" and switchover_type != "rpsw" and switchover_type != "vrp":
            raise E.NodeError("Error type of %s" % switchover_type)
        logger.info("Reloading switch-over %s", switchover_type)
        erv_cli.sendline("reload switch-over %s" % switchover_type)
        ret = erv_cli.expect(expect_list, timeout=500)
        print("Node info: %s", erv_cli.before)
        wait_min = 0
        while wait_min * 60 < 300:
            if ret == 1:
                erv_cli.sendline("y")
                print("Sending yes to really want to reload")
                break

            if ret == 0:
                erv_cli.sendline("n")
                print("Sending no to give up current node conf")

            try:
                ret = erv_cli.expect(expect_list, timeout=60, timeout_handle=False)
            except (E.TimeoutError, E.SessionError):
                wait_min += 1
                print("Waiting %s minutes for the reload", wait_min)
                ret = -1

        if wait_min * 60 >= 300:
            raise E.NodeError("No response from node in %s seconds, reload switch-over failed" % 300)

if __name__ == '__main__':
    target = str(sys.argv[1])
    job = testStart(target)
    job.do()


