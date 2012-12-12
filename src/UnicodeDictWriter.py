#!/usr/bin/python
# -*- coding: utf-8 *-*
__author__="kamilla and maylon"
__date__ ="$Sep 23, 2012 11:29:36 AM$"


import csv
import cStringIO
import codecs
import types


class UnicodeDictWriter(csv.DictWriter):
    ##
    ##A CSV DictWriter which will write rows to CSV file "f",
    ##which is encoded in the given encoding.
    ##

    def __init__(self, f, fields, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(
            self.queue, fields, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow(dict(
            (f, v.encode("utf-8") if isinstance(v, types.StringTypes) else v)
                for f, v in row.iteritems()))
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


if __name__ == "__main__":
    main()