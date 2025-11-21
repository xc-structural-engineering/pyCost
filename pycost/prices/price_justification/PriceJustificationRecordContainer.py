# -*- coding: utf-8 -*-
''' Price justification container.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
from pycost.prices.price_justification import PriceJustificationRecord
from pycost.utils import basic_types
from pycost.utils import pylatex_utils

class PriceJustificationRecordContainer(list):
    def __init__(self,tp):
        self.tipo= tp

    def StrTipo(self):
        return basic_types.str_tipo(self.tipo)

    def SetBase(self, b):
        for i in self:
            (i).SetBase(b)

    def SetBaseAcum(self, b):
        if(len(self)):
            base= basic_types.ppl_price(b)
            for i in self:
                (i).SetBase(base)
                base+= (i).getTotal()

    def writePriceJustification(self, data_table):
        ''' Write price justification into a latex table.

        :param data_table: pylatex table to write into.
        '''
        if(len(self)):
            for i in self:
                (i).writePriceJustification(data_table)
            row= [pylatex.table.MultiColumn(4, align='r',data='Total '+self.StrTipo())]
            row.append('')
            row.append(basic_types.human_readable(self.getTotal()))
            data_table.add_row(row)

    def writePriceTableTwoIntoLatexDocument(self, data_table):
        total= self.getTotal()
        if total>basic_types.ppl_price(0.0):
            data_table.add_row(['','',self.StrTipo(),basic_types.human_readable(total)])

    def writePriceTableTwoIntoLatexDocumentPorc(self, os):
        if(len(self)):
            for i in self:
               (i).writePriceTableTwoIntoLatexDocument(os)

    def getTotal(self):
        retval= basic_types.ppl_price(0.0)
        for i in self:
            retval+= (i).getTotal()
        return retval


