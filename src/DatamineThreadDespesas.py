# -*- coding: utf-8 *-*
__author__="kamilla and maylon"
__date__ ="$Sep 23, 2012 2:43:21 PM$"

import threading

class DatamineThreadDespesas(threading.Thread):
    def __init__(self, out_queue_despesas, instance):
        threading.Thread.__init__(self)
        self.out_queue_despesas = out_queue_despesas
        self.instance = instance

    def run(self):
        print "In DATAMINE"
        while True:
            #grabs host from queue
            #pop element from queue to send it to fetchReceitas
            data = self.out_queue_despesas.get()
            print "dataMine: " + str(data)
            self.instance.fetch(data[0], data[1])
            self.out_queue_despesas.task_done()