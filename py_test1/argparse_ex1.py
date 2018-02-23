import argparse

def arg_parse():
    parser = argparse.ArgumentParser(description='load rate limit configuration')
    parser.add_argument('--level', '-l', choices=['apn', 'node'], dest='level')
    parser.add_argument('--rate', '-r', type=int, dest='rate')
    parser.add_argument('--type', '-t', action='append', choices=['create', 'delete'], dest='type')
    parser.add_argument('--interface', '-i', action='append', choices=['s5s8', 'gn'], dest='interface')
    parser.add_argument('--node', '-n', type=str, dest='host')
    parser.add_argument('--clean', '-c', action='store_true', dest='clear')
    parser.add_argument('--debug', '-d', action='store_true', dest='debug')
    parser = parser.parse_args()

    return parser

def main():
    parser = arg_parse()
    host = parser.host
    print host


if __name__ == '__main__':
    main()