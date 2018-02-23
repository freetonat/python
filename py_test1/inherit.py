# diamond3.py

class Client():
    def __init__(self):
        self.name = 'ytson'
        print("Client")

    def init_session(self):
        print("Client.init_session")


class SSRshellClient(Client):
    def init_session(self):
        #super(SSRshellClient, self).init_session()
        super().init_session()
        print("init session")

test = SSRshellClient()
test.init_session()output = '''
Client
Client.init_session
init session
'''
