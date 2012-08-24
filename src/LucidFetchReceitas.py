# -*- coding: utf-8 *-*

## @author Kamilla H. Crozara
#  @date August, 2012
#  @version 1.0

__author__ = "kamilla"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

from ctypes import *
import errno
import sys
import time

import ast
from bs4 import BeautifulSoup
import mechanize
import os
import re

## @class LucidFetchReceitas()
#  This class is responsible for get data from Portal da Transparência
#  do Distrito Federal and save this in CSV format
class LucidFetchReceitas():
    
    ## @var (position)
    #  Item's position in hashtable
    position = 0


    ## Uses ctypes to try to load the C module.
    try:
        load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
    except:
        print "Can't load C module!"
    
    ## @fn Function fetch(self, BASE_URL, br) request data and categorize it
    #  @param <BASE_URL> {Is the link for get data}
    #  @param <br> {Is the browser from mechanizer}
    def fetch(self, BASE_URL, br):
        
        ## @var (html)
        #  is the result from the request to the BASE_URL
        html = br.open(BASE_URL).get_data()
        #print html

        ## Tries to call a function from C module to create a new hashset
        #  The hashset created get follow parameters:
        #   @param <sys.getsizeof(str)> {Size of some string in Python}
        #   @param <totalRows> {Number of rows from file that was downloaded}
        try:
            ## @var (totalRows)
            #  is the number of rows from file that was downloaded
            totalRows = int(re.search('[0-9]', re.search('"totalRows":[0-9]', html).group()).group())
            self.load.Py_HashSetNew(sys.getsizeof(str), totalRows)
        except:
            print "Can't load C module to create a new HashSet."

        ## @var (labels)
        #  are the labels from file that was download
        #  it iterates over the result and gets the labels
        labels = []
        for s in re.findall('("[A-Z]+")', html):
            text = re.search('[\d\w\s]+', s).group()
            if not any(text in title for title in labels):
                labels.append(text)

        ## Convert labels into string and try to put it into the getPosition
        #  in hashtable
        self.putItemInHash(', '.join(labels), self.getPosition())

        
        ## @var (rows)
        #  Are the rows from file that was download
        #  it iterates over the result and gets the labels
        rows = []
        result = re.findall('(:\"[\d\w\s]+"|:[\d\w\s.]+)', html)
        for i in range(3, len(result)):
            rows.append(re.search('[\d\w\s.]+', result[i]).group())

        #print rows
        #print ', '.join(re.findall('[\d\w\s.]+',result[i]))
        #print ', '.join(rows)

        #data = ast.literal_eval(html)

        try:
            self.load.Py_PrintFn()
        except:
            print "Can't load C module to print elements from HashSet."

        try:
            self.load.HashSetDispose()
        except:
            print "Can't load C module to free memory."

    def putItemInHash(self, item, position):
        print type(item)
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

    def storeData(self):
        self.verifyFolder("incomeToGDF")
        #try:
            #CDLL("libc.so.6")
            #load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
        #except:
            #print "Can't load C module!"

        self.load.storeData()
        
        #soup = BeautifulSoup(html)
        #print soup.select(".colunaValor")
        #try:
            #f = open('./transferedToGDF/transferedToGDF' + str(self.getNumFiles()) + self.getDateTime(), 'w')
            #for s in html:
                #f.write(s)
            #f.close()
            #self.setNumFiles(self.getNumFiles() + 1)
        #except IOError:
            #print "Error: can\'t find file or write data"


    def verifyFolder(self, pathName):
        try:
            if not os.path.exists(pathName):
                os.makedirs(pathName)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return "Maybe you don't have permission to access this folder"

    #def getDateTime(self):
        #localtime = time.asctime(time.localtime(time.time()))
        #return str(localtime)

    #def getNumFiles(self):
        #return self.numFiles

    #def setNumFiles(self, numFiles):
        #self.numFiles = numFiles

    #def getNextPage(self, BASE_URL, html):
        #nextPage = BASE_URL + "&Pagina=" + str(self.getNumFiles())
        #return nextPage
