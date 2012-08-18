# -*- coding: utf-8 *-*
__author__ = "kamilla"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

import time
import mechanize
import errno
import os
from bs4 import BeautifulSoup
import ast
import sys

#The ctypes interface by default only handles Python integer, long, and string
#data types. If you use float or something else then you must tell ctypes how
#to convert the C function call arguments and result value.
from ctypes import *
#import moduleVectorHash


class LucidFetchReceitas():
    def fetch(self, BASE_URL, br):
        html = br.open(BASE_URL).get_data()
        data = ast.literal_eval(html)
    
        try:
            libc = CDLL("libc.so.6")
            load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
        except:
            print "Can't load C module!"

        try:
            load.Py_HashSetNew(sys.getsizeof(str), data.get('response').get('totalRows'))
        except:
            print "Can't load C module to create a new HashSet."
            
        position = 0
        for s in data.get('response').get('data'):
                try:
                    myString = c_char_p(str(s))
                    myStringAddr = cast(myString, c_void_p)
                    load.Py_HashSetEnter(myStringAddr, position)
                    position = position + 1
                except:
                    print "Can't save element in hash"

        try:
            load.Py_PrintFn()
        except:
            print "Can't load C module to print elements from HashSet."

        #try:
            #load.HashSetDispose()
        #except:
            #print "Can't load C module to free memory."

    def storeData(self, html):
        self.verifyFolder("incomeToGDF")
        
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

    def getDateTime(self):
        localtime = time.asctime(time.localtime(time.time()))
        return str(localtime)

    def getNumFiles(self):
        return self.numFiles

    def setNumFiles(self, numFiles):
        self.numFiles = numFiles

    def getNextPage(self, BASE_URL, html):
        nextPage = BASE_URL + "&Pagina=" + str(self.getNumFiles())
        return nextPage
