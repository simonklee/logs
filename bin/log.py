#!/usr/bin/env python

import sys
import logs
import optparse
import logging

if __name__ == '__main__':
    opts = optparse.OptionParser(usage="usage: %prog [options] <filename>")
    opts.add_option('--min-threshold', default=100.0, type='float',
            help='min threshold value to consider')
    opts.add_option('--min-count', default=10, type='int',
            help='min occurence count to consider')
    opts.add_option('-l', '--log-level', type='choice', action='store',
            dest='level', choices=('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'),
            default='ERROR', help='Log level to use',)
    (options, args) = opts.parse_args()
    logging.basicConfig(level=options.level)

    try:
        if len(args) == 1:
            fp = open(args[0], 'r')
        else:
            fp = sys.stdin

        analyzer = logs.Analyzer(fp, min_threshold=options.min_threshold, min_count=options.min_count)
        logs.fmt(analyzer.percentile())
    finally:
        fp.close()
