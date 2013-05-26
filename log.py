from __future__ import print_function

import sys
import numpy

entries = {}

def avg(N):
    return sum(N)/len(N)

def entry(url, msecs):
    if not url in entries:
        entries[url] = []

    entries[url].append(msecs)

def analyze(filename):
    with open(filename) as fp:
        for line in iter(fp):
            items = line.split(' ')

            if len(items) < 24:
                continue

            entry(' '.join(items[16:18]), int(items[23]))

    out = []

    for url, values in entries.iteritems():
        if len(values) < 10:
            continue

        eight=numpy.percentile(values, 90)
        if eight > 100.0:
            out.append((eight, url, len(values)))

    out.sort(key=lambda v: v[0])

    for v, url, count in out:
        print('{}'.format(url))
        print('90% read in {} msecs (count {})'.format(v, count))
        print('')
        #print(url, len(values), eight, avg(values))

if __name__ == '__main__':
    analyze(sys.argv[1])
