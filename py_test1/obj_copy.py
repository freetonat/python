import copy

class Peer():

    def __init__(self, succeed, failed):
        self.succeed = succeed
        self.failed = failed
        print self
        print self.succeed
        print self.failed


if __name__ == '__main__':
    org_dic = {}
    dup_dic = {}
    aaa = Peer(1, 2)
    bbb = Peer(11, 22)
    org_dic['gx-1'] = aaa
    org_dic['gx-2'] = bbb
    print org_dic

    #key_list = org_list.keys()

    for i in org_dic.keys():
        print('{}: succeed = {}, failed = {}'.format(i, org_dic[i].succeed, org_dic[i].failed))

    dup_dic = copy.deepcopy(org_dic)
    print dup_dic

    org_dic.clear()

    aaa = Peer(5, 6)
    bbb = Peer(61, 71)

    org_dic['gx-1'] = aaa
    org_dic['gx-2'] = bbb
    print org_dic

    for i in org_dic.keys():
        print('{}: diff_succeed = {}, diff_failed = {}'.format(i, org_dic[i].succeed - dup_dic[i].succeed, org_dic[i].failed - dup_dic[i].failed)),
        print 'kkk'

