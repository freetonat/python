#! /usr/bin/env python
__author__ ='eyonson'
__version__ = '1.0'
import sys
sys.path.insert(0, '/home/eyonson/CLI_R5A42/src')
#sys.path.insert(0, '/home/eyonson/CLI_R5A42/epgcats/tcdb/LIB_general/Robustness')
sys.path.insert(0, '/home/eyonson/CLI_R5A42/epgcats/tcdb')
import time
import re
import autott.session
import simtool.blade
import StringIO
import LIB_general.Robustness.ext_rob

class send_cli():

    def __init__(self, target):
        self.target = target
        self.node = autott.session.SSRNode(self.target)
        self.blade = 'epgtool'+self.target[3:]+'0'
        self.tool = simtool.blade.Blade(self.blade)

    def do(self):
        oam_cli = self.node.oam_cli
        erv_cli = self.node.erv_cli
        shell_cli = self.node.shell_cli
        blade_cli = self.tool.bladecli

        #From here insert command
        #erv_cli.do('show chassis')
        mme_list = []
        output = blade_cli.do('lts_list_mme all')
        for line in StringIO.StringIO(output):
            line = line.strip()
            #mat = (re.search(r'(\d+)\s+(\d+.\d+.\d+.\d+)', line))
            mat = (re.search(r'(\d+)\s+(\d+.\d+.\d+.\d+)\s+(\w+:\w+:\w+:\w+:\w+:\w+:\w+:\w+)', line))
            #mat = (re.search(r'(\d+)\s+(\S*)\s+(\S*)', line))
            if mat:
                mme_list.append(mat.group(2))
                mme_list.append(mat.group(3))
        #print(mme_list)
        #print(len(mme_list))
        j=1
        cnt=1
        for i in mme_list:
            if cnt%6 == 0:
                j=j+1
            self.node.run_oam(["ManagedElement=1", "Epg=1", "Sgw=1", "Interface=1", "S4s11C=1", "NetworkRestorationPool=Rstpool_%d" % j, "NetworkElement=Element_%d" % cnt, "address=%s" % i], 1)
            self.node.run_oam(["ManagedElement=1", "Epg=1", "Sgw=1", "Interface=1", "S4s11C=1", "NetworkRestorationPool=Rstpool_%d" % j, "NetworkElement=Element_%d" % cnt, "priority=0"], 1)
            cnt = cnt+1

target = str(sys.argv[1])     # target is epgx-x
sending_cli = send_cli(target)
sending_cli.do()
