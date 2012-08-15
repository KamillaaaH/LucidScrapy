# -*- coding: utf-8 *-*
__author__="kamilla"
__date__ ="$Aug 1, 2012 10:52:37 AM$"

import time
import mechanize
import errno
import os
from bs4 import BeautifulSoup
import ast
from ctypes import *


class LucidFetchReceitas():
    numFiles = 1

    def fetch(self, BASE_URL, br):
        html = br.open(BASE_URL).get_data()
        dict = ast.literal_eval(html)

        try:
            load = cdll.LoadLibrary('./moduleVectorHash.so')
        except:
            print "Can't load C module!"
        
        load.CreateNewHashPy(len(dict), 10)

        for s in dict.get('response').get('data'):
            try:
                load.EnterItemPy(str(s))
            except:
                print "Can't save element in hash"

        load.

            

    def storeData(self, html):
        self.verifyFolder("transferedToGDF")
        soup = BeautifulSoup(html)
        print soup.select(".colunaValor")
        try:
            f = open('./transferedToGDF/transferedToGDF' + str(self.getNumFiles()) + self.getDateTime(), 'w')
            for s in html:
                f.write(s)
            f.close()
            self.setNumFiles(self.getNumFiles() + 1)
        except IOError:
            print "Error: can\'t find file or write data"


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
