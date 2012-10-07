# -*- coding: utf-8 *-*
__author__ = "kamilla"
__date__ = "$Oct 4, 2012 4:44:16 PM$"

import os
import errno
import sys
import mechanize
import cookielib
import glob
import csv

class Util():

    def verifyFolder(self, pathName):
        try:
            if not os.path.exists(pathName):
                os.makedirs(pathName)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
            return "Maybe you don't have permission to access this folder"

    def getFileName(self, pathName, fileName):
        return pathName + "/" + str(fileName) + ".csv"


    def getBrowser(self):
        # Browser
        br = mechanize.Browser()
        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        # Browser options
        br.set_handle_equiv(True)
        # br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        # Debugging messages
        br.set_debug_http(True)
        br.set_debug_redirects(True)
        br.set_debug_responses(True)
        # Add http headers
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        return br


    def concatFiles(self, path, fileName):
        rows = []
        for infile in glob.glob(os.path.join(path, '*.csv')):
            csvReader = csv.reader(open(infile, 'r'), delimiter=',')
            c = csv.writer(open(fileName, "wb"))
            for row in csvReader:
                rows.append(row)
            for i in rows:
                c.writerow(i)