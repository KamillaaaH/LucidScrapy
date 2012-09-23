# -*- coding: utf-8 *-*
__author__="kamilla and maylon"
__date__ ="$Sep 23, 2012 11:29:36 AM$"


import json
import csv
import cStringIO
import codecs
import types


class UnicodeDictWriter(csv.DictWriter):
    """
    A CSV DictWriter which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, fields, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(
            self.queue, fields, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow(dict(
            (f, v.encode("utf-8") if isinstance(v, types.StringTypes) else v)
                for f, v in row.iteritems()))
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


#data = '{"response":{"startRow":0,"endRow":5,"totalRows":5,"data":   [{"CODIGO":"72","DESCRICAO":"RECEITA INTRA-ORÇÁMENTÁRIAS DE CONTRIBUÇÕES","PREVISTA":225847716.0,"REALIZADA":165311075.58,"DIFERENCA":60536640.42,"R___":1.0},{"CODIGO":"76","DESCRICAO":"RECEITA  INTRA-ORÇAMENTÁRIAS DE SERVIÇOS","PREVISTA":22367493.0,"REALIZADA":3435363.08,"DIFERENCA":18932129.92,"R___":2.0},{"CODIGO":"77","DESCRICAO":"TRANSFERÊNCIAS  INTRA-ORÇAMENTÁRIAS CORRENTES","PREVISTA":1218252.0,"REALIZADA":0.0,"DIFERENCA":1218252.0,"R___":3.0},{"CODIGO":"71","DESCRICAO":"RECEITA TRIBUTÁRIA INTRA-ORÇAMENTÁRIA","PREVISTA":12000.0,"REALIZADA":0.0,"DIFERENCA":12000.0,"R___":4.0},{"CODIGO":"79","DESCRICAO":"OUTRAS RECEITAS INTRA-ORÇAMENTÁRIAS CORRENTES","PREVISTA":0.0,"REALIZADA":311785.30,"DIFERENCA":-311785.30,"R___":5.0}]}}'
#field_order = [
    #'CODIGO', 'DESCRICAO', 'PREVISTA', 'REALIZADA', 'DIFERENCA', 'R___']

#with open('jsontest.csv', 'w') as csvfile:
   # writer = UnicodeDictWriter(csvfile, field_order)
    #writer.writerows(json.loads(data)['response']['data'])
    