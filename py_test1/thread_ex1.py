import threading

class Messenger(threading.Thread):
    def run(self):
        for _ in range(10):
            print(threading.current_thread().getName())

send = Messenger(name='Sending out message')
receive = Messenger(name='Receiving message')

send.start()
receive.start()
'''
output = 
Sending out message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Sending out message
Receiving message
Receiving message
'''
