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
import ThreadUrl
import DatamineThread
from ctypes import *
import mechanize
import cookielib
import threading
import Queue
import time
import re


hostsReceitas = {'receitas': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Geral&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-0&_dataSource=dsReceitasPorCategoria-0&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_correntes': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=1&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-1&_dataSource=dsReceitasPorCategoria-1&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_capital': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=2&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-2&_dataSource=dsReceitasPorCategoria-2&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_intra_orcamentarias_correntes': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=7&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-3&_dataSource=dsReceitasPorCategoria-3&isc_metaDataPrefix=_&isc_dataFormat=json",
         'receitas_intra_orcamentarias_capital': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=8&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-4&_dataSource=dsReceitasPorCategoria-4&isc_metaDataPrefix=_&isc_dataFormat=json",
         'deducoes_restituicoes_receita': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Categoria&codigo=9&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-5&_dataSource=dsReceitasPorCategoria-5&isc_metaDataPrefix=_&isc_dataFormat=json"}


hostsDespesas = {'despesas_categoria_credor_0': "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=0&_endRow=300&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCredor&_dataSource=dsDespesasOrgaoCredor&isc_metaDataPrefix=_&isc_dataFormat=json"}

    

queue = Queue.Queue()
out_queue = Queue.Queue()

queue_despesas = Queue.Queue()
out_queue_despesas = Queue.Queue()

## Uses ctypes to try to load the C module.
#  @load is the cdll referency that loads dynamic link libraries.
#try:
    #load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
#except:
    #print "Can't load C module!"


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

def getNumberRows():
    br = getBrowser()
    response = br.open("http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCredor&_dataSource=dsDespesasOrgaoCredor&isc_metaDataPrefix=_&isc_dataFormat=json").get_data()
    return int(re.search('[0-9]+', re.search('"totalRows":[0-9]+', response).group()).group())

def queueHostsDespesas():
    numRows = getNumberRows()
    i = 301
    j = 1
    #while i < 300:
    while i <= numRows:
        if i+301 > numRows:
            remainderRows = numRows - i
            key = "despesas_categoria_credor_0" + str(j)
            hostsDespesas.update({key: "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=" + str(i) + "&_endRow=" + str(i+remainderRows) + "&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCred"})
            return
        
        key = "despesas_categoria_credor_0" + str(j)
        hostsDespesas.update({key: "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=" + str(i) + "&_endRow=" + str(i+301) + "&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCred"})
        i = i+301
        j = j+1

def calculateAverageDespesas():
    ## Uses ctypes to try to load the C module.
    #  @load is the cdll referency that loads dynamic link libraries.
    try:
        load = cdll.LoadLibrary('./moduleVectorHash/moduleVectorHash.so')
    except:
        print "Can't load C module!"
        

def getLenHostsReceitas():
    return len(hostsReceitas)

def getLenHostDespesas():
    return len(hostsDespesas)

    
start = time.time()
def main():
    queueHostsDespesas()
    lenHostReceitas = getLenHostsReceitas()
    lenHostDespesas = getLenHostDespesas()
 
    ####
    # Threads to fetch RECEITAS
    ####
    fetchReceitas = LucidFetchReceitas.LucidFetchReceitas()
    #spawn a pool of threads, and pass them queue instance
    for i in range(lenHostReceitas):
        br = getBrowser()
        t = ThreadUrl.ThreadUrl(queue, out_queue, br)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hostsReceitas.items():
        queue.put(host)

    for i in range(lenHostReceitas):
        dt = DatamineThread.DatamineThread(out_queue, fetchReceitas)
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed
    queue.join()
    out_queue.join()
    ####
    # End threads to fetch RECEITAS
    ####

    ####
    # Threads to fetch DESPESAS
    ####
    fetchDespesas = LucidFetchDespesas.LucidFetchDespesas()
    #spawn a pool of threads, and pass them queue instance
    for i in range(lenHostDespesas):
        br = getBrowser()
        t = ThreadUrl.ThreadUrl(queue_despesas, out_queue_despesas, br)
        t.setDaemon(True)
        t.start()

    #populate queue with data
    for host in hostsDespesas.items():
        queue_despesas.put(host)

    for i in range(lenHostDespesas):
        dt = DatamineThread.DatamineThread(out_queue_despesas, fetchDespesas)
        dt.setDaemon(True)
        dt.start()


    #wait on the queue until everything has been processed
    queue_despesas.join()
    out_queue_despesas.join()

    ####
    # End threads to fetch DESPESAS
    ####  
    
main()

print "Elapsed Time: %s " % (time.time() - start)


