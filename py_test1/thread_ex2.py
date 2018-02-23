#! /usr/bin/env python

import time
import threading
import random
from random import randint
import logging
from sys import argv


logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] (%(threadName)-10s) %(message)s')

def countdown(pName,command):
    print("{0} countdown - command{1} ".format(pName,command))
    retry = 0
    while True:
        print("{0}:{1}".format(pName,retry))
        retry += 1
        if retry > randint(5,10):
            break
        time.sleep(1)
    print("{0} ended".format(pName))

def start(pName, t):
    print("starting countdown for: ",pName)
    t.setName(pName)
    t.setDaemon(True)
    t.start()


if __name__ == "__main__":
    tSalad = threading.Thread()
    tBingo = threading.Thread()
    while 1:
        command = int(input("[1 or 2] >"))
        if command == 1 and not tSalad.isAlive():
            tSalad = threading.Thread(target = countdown, args=("Salad", 1))
            start("Salad", tSalad)

        elif command == 2 and not tBingo.isAlive():
            tBingo = threading.Thread(target = countdown, args=("Bingo", 2))
            start("Bingo", tBingo)