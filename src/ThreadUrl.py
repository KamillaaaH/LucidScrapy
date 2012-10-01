# -*- coding: utf-8 *-*
__author__="kamilla and maylon"
__date__ ="$Sep 23, 2012 2:43:07 PM$"

import threading

class ThreadUrl(threading.Thread):
    def __init__(self, queue, out_queue, br):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
        self.br = br


    def run(self):
        while True:
            host = self.queue.get()
            ## @data
            #  is the result from the request to the urls in hosts
            data = self.br.open(host[1]).get_data()

            if None == data:
                return

            #create a list with the name of category and the data
            chunk = []
            chunk.append(host[0])
            chunk.append(data)
            #put list in out_queue
            self.out_queue.put(chunk)
            self.queue.task_done()