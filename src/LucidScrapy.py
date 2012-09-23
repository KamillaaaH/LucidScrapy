# -*- coding: utf-8 *-*
__author__="kamilla e maylon"
__date__ ="$Aug 1, 2012 10:52:37 AM$"

## @authors Kamilla H. Crozara and Maylon Felix
#  @date August, 2012
#  @version 1.0
#  @filename LucidScrapy.py

## \mainpage Lucid Scrapy Index
#
# \section intro_sec Introduction
#
# This is a project about government open data that
# uses Python to get information about expenses from Governo do
# Distrito Federal (Brazil).
#
# \section install_sec Installation
#
# \subsection step1 Step 1: Opening the box
#
# etc...
#/

import LucidFetchReceitas
import LucidFetchDespesas
from ctypes import *
import mechanize
import cookielib
import threading
import Queue
import json
import time
import re
import UnicodeDictWriter

hosts = {'receitas': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Geral&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-0&_dataSource=dsReceitasPorCategoria-0&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_correntes': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=1&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-1&_dataSource=dsReceitasPorCategoria-1&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_capital': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=2&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-2&_dataSource=dsReceitasPorCategoria-2&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_intra_orcamentarias_correntes': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=7&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-3&_dataSource=dsReceitasPorCategoria-3&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_intra_orcamentarias_capital': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=8&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-4&_dataSource=dsReceitasPorCategoria-4&isc_metaDataPrefix=_&isc_dataFormat=json",
         'deducoes_restituicoes_receita': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=9&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-5&_dataSource=dsReceitasPorCategoria-5&isc_metaDataPrefix=_&isc_dataFormat=json"}

queue = Queue.Queue()
out_queue = Queue.Queue()

## Uses ctypes to try to load the C module.
#  @load is the cdll referency that loads dynamic link libraries.
try:
    load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
except:
    print "Can't load C module!"

class ThreadUrl(threading.Thread):
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue
        
    def run(self):
        while True:
            host = self.queue.get()
            br = getBrowser()
            ## @data
            #  is the result from the request to the urls in hosts
            data = br.open(host[1]).get_data()

            #create a list with the name of category and the data
            chunk = []
            chunk.append(host[0])
            chunk.append(data)

            #put list in out_queue
            self.out_queue.put(chunk)
            self.queue.task_done()


class DatamineThread(threading.Thread):
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def run(self):
        while True:
            #grabs host from queue
            #pop element from queue to send it to fetchReceitas
            data = self.out_queue.get()
       
            fetchReceitas = LucidFetchReceitas.LucidFetchReceitas()
            fetchReceitas.fetch(data[0], data[1])
           
            
            self.out_queue.task_done()
            

def getBrowser():
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

start = time.time()
def main():

    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(queue, out_queue)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hosts.items():
        queue.put(host)

    for i in range(5):
        dt = DatamineThread(out_queue)
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed
    queue.join()
    out_queue.join()
  
    
main()
print "Elapsed Time: %s " % (time.time() - start)