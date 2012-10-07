# -*- coding: utf-8 *-*

## @author Kamilla H. Crozara and Maylon Felix
#  @date August, 2012
#  @version 1.0
#  @filename LucidFetchReceitas.py

__author__ = "kamilla e maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

import json
import re
import UnicodeDictWriter
import Util
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
        util = Util.Util()
        util.verifyFolder(pathName)
        fileName = pathName + "/" + str(category) + ".csv"


        with open(fileName, 'w') as csvfile:
            labelWriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            #labelWriter.writerow(labels)
            writer = UnicodeDictWriter.UnicodeDictWriter(csvfile, labels)
            writer.writerows(json.loads(response)['response']['data'])