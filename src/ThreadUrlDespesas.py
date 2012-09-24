# -*- coding: utf-8 *-*
__author__="kamilla and maylon"
__date__ ="$Sep 23, 2012 2:43:07 PM$"

import threading

class ThreadUrlDespesas(threading.Thread):
    def __init__(self, queue_despesas, out_queue_despesas, br):
        threading.Thread.__init__(self)
        self.queue_despesas = queue_despesas
        self.out_queue_despesas = out_queue_despesas
        self.br = br


    def run(self):
        while True:
            host = self.queue_despesas.get()
            ## @data
            #  is the result from the request to the urls in hosts
            data = self.br.open(host[1]).get_data()

            #create a list with the name of category and the data
            chunk = []
            chunk.append(host[0])
            chunk.append(data)

            #put list in out_queue
            self.out_queue_despesas.put(chunk)
            self.queue_despesas.task_done()