# -*- coding: utf-8 *-*
__author__="kamilla"
__date__ ="$Aug 1, 2012 10:52:37 AM$"

import LucidFetchFromUniao
import LucidFetchFromGDF
import mechanize
import cookielib

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

BASE_URL_UNIAO = "http://www.portaltransparencia.gov.br/PortalTransparenciaListaAcoes.asp?Exercicio=2012&SelecaoUF=1&SiglaUF=DF&NomeUF=DISTRITO%20FEDERAL&CodMun=9701&NomeMun=BRASILIA"
uniao = LucidFetchFromUniao.LucidFetchFromUniao()
uniao.fetch(BASE_URL_UNIAO, br)

#BASE_URL_GDF = "http://www.transparencia.df.gov.br/_layouts/Br.Gov.Df.Stc.SharePoint/servicos/Despesas/ServicoGradeDespesasOrgaoCredor.ashx?tipoApresentacao=consulta&exercicio=2012&_operationType=fetch&_startRow=0&_endRow=75&_textMatchStyle=substring&_componentId=gradeDespesasOrgaoCredor&_dataSource=dsDespesasOrgaoCredor&isc_metaDataPrefix=_&isc_dataFormat=json"
#gdf = LucidFetchFromGDF.LucidFetchFromGDF()
#gdf.fetch(BASE_URL_GDF, br)
