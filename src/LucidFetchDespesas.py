# -*- coding: utf-8 *-*
__author__ = "kamilla"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

import time
import mechanize
import cookielib
import errno
import os
import re


class LucidFetchDespesas():
    numFiles = 1
    startRow = 1
    endRow = 500

    def fetch(self, BASE_URL, br):
        print "\n\n ============= Getting data from rows numbers " + str(self.getStartRow()) + " to " + str(self.getEndRow()) + " ============="
        html = br.open(BASE_URL).get_data()
        self.writeData(html)
        regexNumRows = re.compile('[0-9]+')
        regexTotalRows = re.compile('("totalRows":)([0-9]+)')
        totalRows = int(regexNumRows.search(regexTotalRows.search(html).group(0)).group(0))
        count = 1
        while(count <= totalRows):
            try:
                nextPage = self.getNextPage(BASE_URL, html)
                print "\n\n ============= Getting data from rows numbers " + str(self.getStartRow()) + " to " + str(self.getEndRow()) + " ============="
                html = br.open(nextPage).get_data()
                self.writeData(html)
                count = count + 500
            except mechanize.HTTPError, e:
                print str(e.code) + " - Internal Server Errror"
                break

    def writeData(self, html):
        self.verifyFolder("expensedByGDF")
        try:
            f = open('./expensedByGDF/expensedByGDF' + str(self.getNumFiles()) + " - " + self.getDateTime(), 'w')
            print "\n\nWriting data..."
            for s in html:
                f.write(s)
            f.close()
            print "\nFinished to write data..."
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

    def getStartRow(self):
        return self.startRow

    def setStartRow(self, startRow):
        self.startRow = startRow

    def getEndRow(self):
        return self.endRow

    def setEndRow(self, endRow):
        self.endRow = endRow


    def getNextPage(self, BASE_URL, html):
        firstPart = "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_"
        lastPart = "&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCredor&_dataSource=dsDespesasOrgaoCredor&isc_metaDataPrefix=_&isc_dataFormat=json"
        self.setStartRow(self.getStartRow()+ 500)
        self.setEndRow(self.getEndRow() + 500)
        nextPage = firstPart + "startRow=" + str(self.getStartRow()) + "&_endRow=" + str(self.getEndRow()) + lastPart
        return nextPage
