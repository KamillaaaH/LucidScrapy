#!/usr/bin/python
# -*- coding: utf-8 *-*
__author__ = "kamilla e maylon"
__date__ = "$Aug 1, 2012 10:52:37 AM$"

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
import time

import DatamineThread
import LucidFetchDespesas
import LucidFetchReceitas
import Queue
import ThreadUrl
import Util
import csv
import glob
import os
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
util = Util.Util()

def getNumberRows():
    br = util.getBrowser()
    response = br.open("http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCredor&_dataSource=dsDespesasOrgaoCredor&isc_metaDataPrefix=_&isc_dataFormat=json").get_data()
    return int(re.search('[0-9]+', re.search('"totalRows":[0-9]+', response).group()).group())

def queueHostsDespesas():
    numRows = getNumberRows()
    i = 301
    j = 1
    #while i < 300:
    while i <= numRows:
        if i + 501 > numRows:
            remainderRows = numRows - i
            key = "despesas_categoria_credor_" + str(j) + "_"
            hostsDespesas.update({key: "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=" + str(i) + "&_endRow=" + str(i + remainderRows) + "&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCred"})
            return

        key = "despesas_categoria_credor_" + str(j) + "_"
        hostsDespesas.update({key: "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=" + str(i) + "&_endRow=" + str(i + 501) + "&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCred"})
        i = i + 501
        j = j + 1


def splitFilesTypeDespesas(path, fileName, pttr, numRow):
    rows = []
    csvReader = csv.reader(open(path, 'r'), delimiter=',', quotechar='|')
    c = csv.writer(open(fileName, "wb"))
    for row in csvReader:
        if (pttr.match(row[numRow])):
            rows.append(row)
                
    for i in rows:
        c.writerow(i)

def splitFilesTypeDespesasDiversas(path, fileName):
    rows = []
    csvReader = csv.reader(open(path, 'r'), delimiter=',', quotechar='|')
    c = csv.writer(open(fileName, "wb"))
    pttr = re.compile(r'(SEC|ADMINISTRAÇÃO|FUNDA|FUNDO|COMPANHIA|INSTITUTO)')
    for row in csvReader:
        if not (pttr.match(row[1])):
            rows.append(row)

    for i in rows:
        c.writerow(i)


def sumDespesas(path, fileName):
    for infile in glob.glob(os.path.join(path, '*.csv')):
        csvReader = csv.reader(open(infile, 'r'), delimiter=',', quotechar='|')
        c = csv.writer(open(fileName, "wb"))
        #c.writerow(labels)
        totalEmpenho = totalPagar = 0
        pttr = re.compile(r'[0-9]+')
        for row in csvReader:
            if (pttr.match(row[2]))  and (pttr.match(row[3])):
                totalEmpenho = totalEmpenho + int(row[2])
                totalPagar = totalPagar + int(row[3])
                
        line = ["01", 'TOTAL EMPENHADO', totalEmpenho]
        c.writerow(line)
        line = ["02", 'TOTAL A PAGAR', totalPagar]
        c.writerow(line)

def sumCategoria(path, fileName):
    c = csv.writer(open(fileName, "wb"))
    #label = ["TIPO", "EMPENHADO", "PAGO"]
    #c.writerow(label)
    for infile in glob.glob(os.path.join(path, '*.csv')):
        csvReader = csv.reader(open(infile, 'r'), delimiter=',', quotechar='|')
        totalEmpenho = totalPagar = 0
        
        pttr = re.compile(r'[0-9]+')
        #pttr = re.compile(r'(SEC|ADMINISTRAÇÃO|FUNDA|FUNDO|COMPANHIA|INSTITUTO)')
        pttrAdm = re.compile(r'ADMINISTRAÇÃO')
        pttrSec = re.compile(r'SEC')
        pttrFundacao = re.compile(r'FUNDA')
        pttrFundo = re.compile(r'FUNDO|\"FUNDO')
        pttrCompanhia = re.compile(r'COMPANHIA')
        pttrInstituto = re.compile(r'INSTITUTO')

        
        for row in csvReader:
            if (pttr.match(row[2]))  and (pttr.match(row[3])):
                #print str(row[2]) + str(row[3])
                totalEmpenho = totalEmpenho + int(row[2])
                totalPagar = totalPagar + int(row[3])

        if(pttrAdm.match(row[1])):
            line = ["01", "ADMINISTRAÇÕES", str(totalEmpenho), str(totalPagar)]
        elif(pttrSec.match(row[1])):
            line = ["02", "SECRETARIAS", str(totalEmpenho), str(totalPagar)]
        elif(pttrFundacao.match(row[1])):
            line = ["03", "FUNDACOES", str(totalEmpenho), str(totalPagar)]
        elif(pttrFundo.match(row[1])):
            line = ["04", "FUNDOS", str(totalEmpenho), str(totalPagar)]
        elif(pttrCompanhia.match(row[1])):
            line = ["05", "COMPANHIAS", str(totalEmpenho), str(totalPagar)]
        elif(pttrInstituto.match(row[1])):
            line = ["06", "INSTITUTOS", str(totalEmpenho), str(totalPagar)]
        else:
            line = ["07", "DIVERSAS", str(totalEmpenho), str(totalPagar)]
        
        c.writerow(line)
        totalEmpenho = totalPagar = 0


start = time.time()
def main():

    queueHostsDespesas()
    lenHostReceitas = len(hostsReceitas)
    lenHostDespesas = len(hostsDespesas)
    ####
    # Threads to fetch RECEITAS
    ####
    fetchReceitas = LucidFetchReceitas.LucidFetchReceitas()
    #spawn a pool of threads, and pass them queue instance
    for i in range(lenHostReceitas):
        br = util.getBrowser()
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
        br = util.getBrowser()
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
    #calculateAverageDespesas()

    ####
    # End threads to fetch DESPESAS
    ####
    

    util.verifyFolder("despesasCategoria")
    pttrAdm = re.compile(r'ADMINISTRAÇÃO')
    pttrSec = re.compile(r'SEC')
    pttrFundacao = re.compile(r'FUNDA')
    pttrFundo = re.compile(r'FUNDO')
    pttrCompanhia = re.compile(r'COMPANHIA')
    pttrInstituto = re.compile(r'INSTITUTO')
    sumDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/dataDespesas", "despesasTotal/despesas_total.csv")
    sumCategoria("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasCategoria", "despesasTotal/despesas_total_categoria.csv")
    util.concatFiles("/home/kamilla/NetBeansProjects/LucidScrapy/src/dataDespesas", "despesasTotal/despesas.csv")
    splitFilesTypeDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_administracao.csv", pttrAdm, 1)
    splitFilesTypeDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_fundacao.csv", pttrFundacao, 1)
    splitFilesTypeDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_secretaria.csv", pttrSec, 1)
    splitFilesTypeDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_fundo.csv", pttrFundo, 1)
    splitFilesTypeDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_companhias.csv", pttrCompanhia, 1)
    splitFilesTypeDespesas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_institutos.csv", pttrInstituto, 1)
    splitFilesTypeDespesasDiversas("/home/kamilla/NetBeansProjects/LucidScrapy/src/despesasTotal/despesas.csv", "despesasCategoria/despesas_diversas.csv")
main()
print "Elapsed Time: %s " % (time.time() - start)

if __name__ == "__main__":
    main()