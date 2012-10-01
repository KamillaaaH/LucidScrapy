# -*- coding: utf-8 *-*
__author__="kamilla and maylon"
__date__ ="$Sep 23, 2012 2:43:21 PM$"

import threading

class DatamineThread(threading.Thread):
    def __init__(self, out_queue, instance):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
        self.instance = instance

    def run(self):
        while True:
            #grabs host from queue
            #pop element from queue to send it to fetchReceitas
            data = self.out_queue.get()
            #print "dataMine: " + str(data)
            self.instance.fetch(data[0], data[1])
            self.out_queue.task_done()