# -*- coding: utf-8 *-*
__author__="kamilla"
__date__ ="$Aug 1, 2012 10:52:37 AM$"

import LucidFetchReceitas
import LucidFetchDespesas
import mechanize
import cookielib
import VerifyDB
from pymongo import Connection
import ast
import json

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


br = getBrowser()

con = Connection('localhost', 27017)



#db = VerifyDB.VerifyDB()
#db.verifyDB(con)


html = br.open("http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Receitas/ServicoGradeReceitasPorCategoria.ashx?tipoApresentacao=consulta&exercicio=2012&tipoCodigo=Geral&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeReceitasPorCategoria-0&_dataSource=dsReceitasPorCategoria-0&isc_metaDataPrefix=_&isc_dataFormat=json").get_data()

try:
    db = con.test_receita
    receitas = db.test_tipo_receita
except:
    print "ERRR 1"

dict = ast.literal_eval(html)
print type(dict)
for s in dict.get('response').get('data'):
    receita = {'codigo':s['CODIGO'], 'descricao': s['DESCRICAO'], 'prevista': s['PREVISTA'], 'realizada': s['REALIZADA']}

print receitas.find({"codigo": "1"})

#jsonFile = json.JSONDecoder().decode(html)
#print type(jsonFile)
#f = open('test', 'w')
#f.write(html)

#decode = ast.literal_eval(html)



#my_dict = {}

#for item in html.split(','):
    #key,value = item.split(':')
    #if my_dict.get( key ):
        #my_dict[ key ] += int( value )
    #else:
        #my_dict[ key ] = int( value )

#print my_dict




#BASE_URL_UNIAO = "http://www.portaltransparencia.gov.br/PortalTransparenciaListaAcoes.asp?Exercicio=2012&SelecaoUF=1&SiglaUF=DF&NomeUF=DISTRITO%20FEDERAL&CodMun=9701&NomeMun=BRASILIA"
#uniao = LucidFetchFromUniao.LucidFetchFromUniao()
#uniao.fetch(BASE_URL_UNIAO, br)

#BASE_URL_GDF = "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCredor&_dataSource=dsDespesasOrgaoCredor&isc_metaDataPrefix=_&isc_dataFormat=json"
#gdf = LucidFetchFromGDF.LucidFetchFromGDF()
#gdf.fetch(BASE_URL_GDF, br)
