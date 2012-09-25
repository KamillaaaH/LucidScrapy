# -*- coding: utf-8 *-*
__author__ = "kamilla and maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

import time
import mechanize
import cookielib
import errno
import os
import re
import UnicodeDictWriter
import json
import csv

class LucidFetchDespesas():
        
    def fetch(self, category, response):
        labels = []
        for s in re.findall('("[A-Z]+")', response, re.U):
            text = re.search('[\d\w\s]+', s).group()
            if not any(text in title for title in labels):
                labels.append(text)
        #print response
        labels.append("R___")
        #print labels
        #codUG = re.findall('([0-9]+)', str(re.findall('("CODIGOUG":"[0-9_.]+")', response, re.U)) , re.U)
        #fileName = str(category) + ".csv"
        #c = csv.writer(open("fileDespesas.csv", "wb"))
        #c.writerow(labels)
        #c.writerow([" "])
        #   c.close()
        pathName = "dataDespesas"
        self.verifyFolder(pathName)
        fileName = pathName + "/" + str(category) + ".csv"

        #verifyFolder(self, dataDespesas)
        #fileName = str(category) + ".csv"
        with open(fileName, 'w') as csvfile:
            labelWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            labelWriter.writerow(labels)
            writer = UnicodeDictWriter.UnicodeDictWriter(csvfile, labels)
            towrite = json.loads(response)['response']['data']
            #codUG = re.search('[0-9]+',str(re.search('(\"CODIGOUG\":\"[0-9]+\")', response).group())).group()
            #print re.split('(\"CODIGOUG\":\"[0-9]+\")', response)
            #print "New codUG: " + str(codUG)
            writer.writerows(towrite)


    def verifyCodUG(self, toWrite):
        codUG = re.findall('[0-9]+',str(re.findall('(u\'CODIGOUG\': u\'[0-9]+\')', str(towrite))))
        

    def verifyFolder(self, pathName):
        try:
            if not os.path.exists(pathName):
                os.makedirs(pathName)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return "Maybe you don't have permission to access this folder"