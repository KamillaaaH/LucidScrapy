# -*- coding: utf-8 *-*

## @author Kamilla H. Crozara and Maylon Felix
#  @date August, 2012
#  @version 1.0
#  @filename LucidFetchReceitas.py

__author__ = "kamilla e maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

from datetime import date
import errno
import sys
import json
import os
import re
import UnicodeDictWriter
import csv

## @class LucidFetchReceitas()
#  This class is responsible for get data from Portal da Transparência
#  do Distrito Federal and save this in CSV format
class LucidFetchReceitas():

    ## @fn fetch(self, BASE_URL, br) request data and categorize it
    #  @param [BASE_URL] is the link for get data
    #  @param [br] Is the browser from mechanizer
    def fetch(self, category, response):
        labels = []
        for s in re.findall('("[A-Z]+")', response):
            text = re.search('[\d\w\s]+', s).group()
            if not any(text in title for title in labels):
                labels.append(text)

        labels.append("R___")

        pathName = "dataReceitas"
        self.verifyFolder(pathName)
        fileName = pathName + "/" + str(category) + ".csv"


        with open(fileName, 'w') as csvfile:
            labelWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            labelWriter.writerow(labels)
            writer = UnicodeDictWriter.UnicodeDictWriter(csvfile, labels)
            writer.writerows(json.loads(response)['response']['data'])

    def verifyFolder(self, pathName):
        try:
            if not os.path.exists(pathName):
                os.makedirs(pathName)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return "Maybe you don't have permission to access this folder"