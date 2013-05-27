from __future__ import print_function, absolute_import

import numpy
import re
import logging

logger = logging.getLogger('logs')

class Analyzer(object):
    def __init__(self, fp, parser=None, min_count=10, min_threshold=100.0):
        '''
        :param fp: file like object of data.
        :param min_count: min occurence count to consider.
        :param min_threshold: min msecs to consider.
        '''
        self.fp = fp
        self.parser = parser or Parser()
        self.min_count = min_count
        self.min_threshold = min_threshold

    @property
    def entries(self):
        if not hasattr(self, '_entries'):
            entries = {}

            for url, msec in self.parser.parse(self.fp):
                if not url in entries:
                    entries[url] = []

                entries[url].append(msec)

            self._entries = entries

        return self._entries

    def percentile(self, percent=90, order='ASC'):
        '''Returns a array of tuples [(msecs, url, count) ..]
        sorted by msecs.

        :param percent: percentile value below which observations fall.
                        Default 90.
        :param order: 'ASC' or 'DESC'. Default 'ASC'.
        '''
        out = []
        min_count = self.min_count
        min_threshold = self.min_threshold

        for url, values in self.entries.iteritems():
            if len(values) < min_count:
                continue

            eight=numpy.percentile(values, 90)

            if eight > min_threshold:
                out.append((eight, url, len(values)))

        out.sort(key=lambda v: v[0])

        if order.upper() == 'DESC':
            out.reverse()

        return out

class Parser(object):
    line_pat = re.compile(r'.* (HEAD|GET|POST|PUT|DELETE) (\S+) .* in (\d+) msecs .*')

    def __init__(self, process_path_cb=None, discard_url_params=True):
        self.process_path_cb = process_path_cb
        self.discard_url_params = discard_url_params

    def parse(self, fp):
        for line in fp:
            row = self.process_line(line)

            if not row:
                continue

            yield row[0], row[1]

    def process_line(self, line):
        res = re.match(self.line_pat, line)

        if not res:
            logger.warning("Can't parse line: {0}".format(line.strip()))
            return None

        if self.discard_url_params:
            path = res.group(2).split('?')[0]
        else:
            path = res.group(2)

        if self.process_path_cb:
            path = self.process_path_cb(path)

        return path, int(res.group(3))
