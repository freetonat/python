#! /usr/bin/env python
__author__ ='eyonson'
"""
./argparse11.py MAKERJ_PATH a 3 3
 3^3 == 27 """

import argparse

parser = argparse.ArgumentParser(description="Simple 'argparse' demo application")
# Ordinary>
parser.add_argument("MAKERJ_PATH")
parser.add_argument("choiceable", choices=['a','b','c'], help="select from one of the choice options")
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")

# Mutually exclusive> user must select only ONE option from group (at this time, -v and -q)
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-q", "--quiet", action="store_true")

args = parser.parse_args()
answer = args.x**args.y

if args.quiet:
    print(answer)
elif args.verbose:
    print("{} to the power {} equals {}".format(args.x, args.y, answer))
else:
    print("{}^{} == {}".format(args.x, args.y, answer))
