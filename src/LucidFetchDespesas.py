# -*- coding: utf-8 *-*
__author__ = "kamilla and maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

import errno
import json
import Queue
import UnicodeDictWriter
import cookielib
import csv
from datetime import date
import mechanize
import os
import re

class LucidFetchDespesas():

    def fetch(self, category, response):
        queueDespesas = Queue.Queue()
        jsonResponse = json.loads(response)['response']['data']
        pathName = "dataDespesas"
        self.verifyFolder(pathName)
        buffCodUG = jsonResponse[0].get('CODIGOUG')
        empenho = pagar = 0
        labels = ['CODIGOUG', 'NOMEUG', 'TOTALEMPENHO', 'TOTALPAGAR']


        for i in range(0, len(jsonResponse)):
            if jsonResponse[i]:
                queueDespesas.put(jsonResponse[i])

        c = csv.writer(open(self.getFileName(pathName, category), "wb"))
        c.writerow(labels)
        while(not queueDespesas.empty()):
            queueElem = queueDespesas.get()
            empenho = empenho + int(queueElem.get('EMPENHO'))
            pagar = pagar + int(queueElem.get('PAGAR'))

            if queueElem.get('CODIGOUG') != buffCodUG:
                #row = str(queueElem.get('CODIGOUG')) + ","  + str(queueElem.get('NOMEUG').encode('ascii', 'ignore'))  + ","  + str(empenho)  + ","  +  str(pagar)
                row = [queueElem.get('CODIGOUG'), queueElem.get('NOMEUG').encode('utf-8'), empenho, pagar]
                #row = {'CODIGOUG' : queueElem.get('CODIGOUG'), 'NOMEUG' : queueElem.get('NOMEUG').encode('ascii', 'ignore'), 'EMPENHO' : empenho, 'PAGAR': pagar}
                if row:
                    c.writerow(row)

                empenho = pagar = 0
                buffCodUG = queueElem.get('CODIGOUG')

    def getFileName(self, pathName, fileName):
        return pathName + "/" + str(fileName) + ".csv"

    def verifyFolder(self, pathName):
        try:
            if not os.path.exists(pathName):
                os.makedirs(pathName)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return "Maybe you don't have permission to access this folder"