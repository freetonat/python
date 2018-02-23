import os
import re
import time

map_record_content = {}

class ParseStatistic(object):

    def __init__(self):
        self.title_dic = {}
        self.value_lines = []
        self.timestamp = []
        self.time_gap = []

    def initialize(self, file_path):
        self._get_file_content(file_path)
        self.get_time()

    def _pmlog_proc_main(self):
        self._proc_compute_picinfo()

    def _get_file_content(self, file_path):
        idx = 0
        with open(file_path) as fd:
            line = fd.readline().strip()
            line = line.split("|")
            print("get_file_content.line = {}".format(line))
            for item in line:
                self.title_dic[item] = idx
                idx += 1
            print(self.title_dic)
            fd.readline()
            lines = fd.readlines()
            for line in [t.strip() for t in lines]:
                data_line_list = line.split("|")
                self.value_lines.append(tuple(data_line_list))

    def get_time(self):
        time_data = []
        for col in self.value_lines:
            epoch = int(time.mktime(time.strptime(col[0], '%Y-%m-%d %H:%M:%S')))
            time_data.append(epoch)
        self.time_gap = [(time_data[t + 1] - time_data[t]) for t in range(len(time_data) - 1)]
        self.timestamp = [time_data[t] - time_data[0] for t in range(len(time_data))]

    def curves_re(self, re_key):
        return [n for n in self.title_dic.keys() if re.search(r'%s' % re_key, n)]

    def curves_list(self, keylist):
        return [n for n in self.title_dic.keys() if n in keylist]

    def mean_counters(self, t):
        s = []
        rest = self.title_dic["gc-0/5/1-averageCpuUsage"]
        print('rest = %s' %rest)
        #print(self.value_lines)
        for col in self.value_lines:
            #print("ytson mean_counters, col = {}".format(col))

            r = [col[self.title_dic[a]] for a in t]
            #print(r)
            if '' in r:
                continue
            s.append(sum([float(b) for b in r]) / len(r))
        return s

    def sumall_counters(self, t):
        s = []
        for col in self.value_lines:
            r = [col[self.title_dic[a]] for a in t]
            if '' in r:
                continue
            s.append(sum([float(b) for b in r]))
        return s

    def dt_counters(self, data):
        return [(data[t + 1] - data[t]) / self.time_gap[t] for t in range(len(data) - 1)]

class DctRecorderGen():

    def __init__(self):
        self._status_all = None
        self._nc_key = "SC (gsc) "
        self._sc_key = "SC "
        self._sp_key = "SC "
        self._pp_key = "PP "

    def initialize(self):
        #pdc_dir = 'C:\Temp'
        pdc_dir = '/Users/freetonat/python'
        status_file = os.path.join(pdc_dir, "pdc_node_status_all.log")
        print("status_file = {}".format(status_file))

        if os.path.isfile(status_file):
            self._status_all = ParseStatistic()
            print("self._status_all = {}".format(self._status_all))
            self._status_all.initialize(status_file)

    def _proc_compute_picinfo(self):
        acpulist = self._status_all.curves_re("-averageCpuUsage")
        print("ytson _proc_compute_picinfo. acpulist = {}".format(acpulist))
        nc_pic, sc_list, sp_list, pp_list = self._get_board_info()
        self._set_nc_info(nc_pic, acpulist)

    def _get_board_info(self):
        funlist = self._status_all.curves_re("-function-name")
        nc_dic = {}
        sc_brd = []
        sc_fun = []
        sp_brd = []
        sp_fun = []
        pp_brd = []
        pp_fun = []
        for pic in funlist:
            if pic.count("Global"):
                nc_dic[pic.split('_')[0]] = [pic.split('_')[1]]
            if pic.count("GW Session") and not pic.count("Secondary"):
                sc_brd.append(pic.split('_')[0])
                sc_fun.append(pic.split('_')[1])
            if pic.count("Packet"):
                pp_brd.append(pic.split('_')[0])
                pp_fun.append(pic.split('_')[1])
            if pic.count("Secondary"):
                sp_brd.append(pic.split('_')[0])
        if nc_dic.keys()[0] in sc_brd:
            idx = sc_brd.index(nc_dic.keys()[0])
            nc_dic[nc_dic.keys()[0]].append(sc_fun[idx])
            sc_brd.remove(nc_dic.keys()[0])
            sc_fun.pop(idx)
        for brd in sp_brd:
            if brd in sc_brd:
                idx = sc_brd.index(brd)
                sp_fun.append(sc_fun[idx])
                sc_brd.remove(brd)
                sc_fun.pop(idx)
        self._set_counter_name(nc_dic.values()[0], sc_fun, sp_fun)

        return nc_dic.keys()[0], sc_brd, sp_brd, pp_brd

    def _set_counter_name(self, nc_lst, sc_lst, sp_lst):
        has_pgw, has_sgw = "", ""
        for i in nc_lst:
            if i.count("PGW"):
                has_pgw = "(psc) "
            if i.count("SGW"):
                has_sgw = "(ssc) "
        self._nc_key = self._nc_key + has_sgw + has_pgw

        has_pgw, has_sgw = "", ""
        for i in sc_lst:
            if i.count("PGW"):
                has_pgw = "(psc) "
            if i.count("SGW"):
                has_sgw = "(ssc) "
        self._sc_key = self._sc_key + has_sgw + has_pgw

        has_pgw, has_sgw = "", ""
        for i in sp_lst:
            if i.count("PGW"):
                has_pgw = "(psc) "
            if i.count("SGW"):
                has_sgw = "(ssc) "
        self._sp_key = self._sp_key + has_sgw + has_pgw

        has_pgw, has_sgw = "", ""
        for i in sc_lst:
            if i.count("PGW"):
                has_pgw = "(ppp) "
            if i.count("SGW"):
                has_sgw = "(spp) "
        self._pp_key = self._pp_key + has_sgw + has_pgw

    def _set_nc_info(self, nc_pic, acpulist):
        real_nacpu = [t for t in acpulist if t.split("-ave")[0] == nc_pic]
        print('real_nacpu = {}'.format(real_nacpu))
        nacpu = self._status_all.mean_counters(real_nacpu)
        print("nacpu = {}".format(nacpu))
        map_record_content["%scpu(AVG)" % self._nc_key] = sum(nacpu) / len(nacpu)
        print('map_record_content = {}'.format(map_record_content))

if __name__ == '__main__':
    record_dct = DctRecorderGen()
    record_dct.initialize()
    record_dct._proc_compute_picinfo()output = '''
status_file = /Users/freetonat/python\pdc_node_status_all.log
'''
