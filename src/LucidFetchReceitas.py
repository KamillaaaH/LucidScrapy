# -*- coding: utf-8 *-*

## @author Kamilla H. Crozara and Maylon Felix
#  @date August, 2012
#  @version 1.0
#  @filename LucidFetchReceitas.py

__author__ = "kamilla e maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

from ctypes import *
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
    ## @position
    #  Item's position in hashtable
    #position = 0
    
    ## Uses ctypes to try to load the C module.
    #  @load is the cdll referency that loads dynamic link libraries.
    #try:
        #load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
    #except:
        #print "Can't load C module!"
    
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

        ## Tries to call a function from C module to create a new hashset
        #  The hashset created gets follow parameters:
        #   @sys.getsizeof(str) is the size of some string in Python
        #   @totalRows is the number of rows from file that was downloaded
        #try:
            ## @totalRows
            #  is the number of rows from file that was downloaded
            #totalRows = int(re.search('[0-9]', re.search('"totalRows":[0-9]', html).group()).group())
            #self.load.Py_HashSetNew(sys.getsizeof(str), totalRows + 1)
        #except:
            #print "Can't load C module to create a new HashSet."
        
        ## @labels
        #  are the labels from file that was download
        #  it iterates over the result and gets the labels
        #labels = []
        #for s in re.findall('("[A-Z]+")', response):
        #    text = re.search('[\d\w\s]+', s).group()
        #    if not any(text in title for title in labels):
        #        labels.append(text)

        #labels.append("ID")
        
        #print labels
        ## Convert @labels into string and try to put it into the getPosition
        #  in hashtable
        #self.putItemInHash(', '.join(labels), self.getPosition())
        #print self.getPosition()

        #i = 0
        #numItemsInRow = 0
        #for i in range(3, len(result)):
            #   rows.append(re.search('[^":]+', result[i]).group())
            #   numItemsInRow = numItemsInRow + 1
            #   if numItemsInRow == len(labels):
                #self.putItemInHash(', '.join(rows), self.getPosition())
                #print rows
            #       rows = []
            #      numItemsInRow = 0
            #       i = i + 1

        #self.load.storeData(self.load.getFilePointer(categoria))


    def verifyFolder(self, pathName):
        try:
            if not os.path.exists(pathName):
                os.makedirs(pathName)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return "Maybe you don't have permission to access this folder"

    ## @fn putItemIhHash(self, item, position) request data and categorize it
    #  @param [item] is the item to put in hashtable
    #  @param [position] is the position that the item is pushed
    def putItemInHash(self, item, position):
        try:
            itemChar = c_char_p(item)
            itemVoidPtr = cast(itemChar, c_void_p)
            self.load.Py_HashSetEnter(itemVoidPtr, position)
            self.setPosition(self.getPosition() + 1)
        except:
            print "Can't save element in hash"

    def setPosition(self, _position):
        self.position = _position

    def getPosition(self):
        return self.position

    def HashSetDispose(self):
        try:
            self.load.HashSetDispose()
        except:
            print "Can't load C module to free memory."

    def storeData(self, categoria):
        print "Let's store it"
        categoriaChar = c_char_p(categoria)
        self.load.storeData(categoriaChar)

    