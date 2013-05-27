import fcntl
import struct
import sys
import termios

def cols():
    return struct.unpack('hh',  fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))[1]

def bold(msg):
    return "\033[1m%s\033[0m" % msg

def clear():
    """Clear screen, return cursor to top left"""
    sys.stdout.write('\033[2J')
    sys.stdout.write('\033[H')

def avg(N):
    return sum(N)/len(N)

def fmt(data, w=None):
    if w is None:
        w = sys.stdout

    for v, url, count in data:
        w.write('{}\n'.format(url))
        w.write('{} msecs (count {})\n\n'.format(v, count))
        #print(url, len(values), eight, avg(values))

