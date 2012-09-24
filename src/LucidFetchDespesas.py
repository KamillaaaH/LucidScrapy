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

        labels.append("R___")
        print response
        #codUG = re.findall('([0-9]+)', str(re.findall('("CODIGOUG":"[0-9_.]+")', response, re.U)) , re.U)
        #fileName = str(category) + ".csv"
        #c = csv.writer(open("fileDespesas.csv", "wb"))
        #c.writerow(labels)
        #c.writerow([" "])
        #   c.close()
        
        fileName = str(category) + ".csv"
        with open(fileName, 'w') as csvfile:
            writer = UnicodeDictWriter.UnicodeDictWriter(csvfile, labels)
            writer.writerows(json.loads(response)['response']['data'])            