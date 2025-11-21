# -*- coding: utf-8 -*-
'''Something that can return the quantities for a unit price.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
import logging
from pycost.prices import unit_price_report
from pycost.measurements import measurement_detail
from pycost.utils import basic_types
from pycost.utils import EntPyCost as epc
from pycost.utils import pylatex_utils

class UnitPriceQuantitiesBase(epc.EntPyCost):

    def __init__(self,u):
        super(UnitPriceQuantitiesBase,self).__init__()
        self.ud= u

    def getUnitPriceCode(self):
        return self.ud.Codigo()

    def UnidadMedida(self):
        return self.ud.Unidad()

    def getUnitPrice(self):
        return self.ud.getPrice()

    def getUnitRoundedPrice(self):
        return self.ud.getRoundedPrice()

    def Informe(self):
        return unit_price_report.UnitPriceReport(self.ud,self.getTotal())

    def getUnitPriceString(self):
        return self.ud.getPriceString()

    def getUnitLtxPriceString(self):
        return self.ud.getLtxPriceString()

    def getPrice(self):
        return self.getTotal()*float(self.ud.getPrice())

    def getRoundedPrice(self):
        retval= self.getRoundedTotal()
        retval*= self.getUnitRoundedPrice()
        return retval.quantize(self.ud.places)

    def getLtxPriceString(self):
        return basic_types.human_readable_currency(self.getRoundedPrice())

    def printLatexHeader(self, data_table, totalr, ancho):
        '''Prints header in the quantities table.'''
        row= [pylatex_utils.ascii2latex(self.getUnitPriceCode())]
        row.append(str(totalr))
        row.append(' ' + pylatex_utils.ascii2latex(self.UnidadMedida()))
        row.append((pylatex.table.MultiColumn(3,align= pylatex.utils.NoEscape(ancho),data= pylatex.utils.NoEscape('\\scriptsize '+pylatex_utils.ascii2latex(self.ud.getNoEmptyDescription())+ '\\normalsize'))))
        data_table.add_row(row)

    def ImprCompLtxMed(self, doc, other):
        '''Imprime la partida.

        :param doc: pylatex document to write into.
        :param other: project to compare with.
        '''
        doc.add_empty_row()
        totalr_other= human_readable(other.getRoundedTotal())
        other.printLatexHeader(os,totalr_other,"p{4.5cm}|")
        doc.append(pylatex_utils.ltx_ampsnd)
        totalr_esta= basic_types.human_readable(getRoundedTotal())
        printLatexHeader(os,totalr_esta,"p{4.5cm}")
        doc.append(pylatex_utils.ltx_fin_reg + '\n')
        ImprLtxLeyenda(doc)
        doc.append(pylatex_utils.ltx_ampsnd)
        ImprLtxLeyenda(doc)
        doc.append(pylatex_utils.ltx_fin_reg + '\n' + pylatex_utils.ltx_hline + '\n')
        quantities.ImprCompLtx(os,other.quantities)
        ImprLtxPie(os,totalr_other)
        doc.append(pylatex_utils.ltx_ampsnd)
        ImprLtxPie(os,totalr_esta)
        doc.append(pylatex_utils.ltx_fin_reg + '\n')
        doc.append(pylatex_utils.ltx_hline + '\n')
        doc.add_empty_row()


    def ImprCompLtxMed(self, doc):
        '''Imprime la partida.

        :param doc: pylatex document to write into.
        :param other: project to compare with.
        '''        
        media_empty_line= ['','', '', '', '', '']
        doc.add_empty_row()
        doc.append(media_empty_line)
        totalr= human_readable(self.getRoundedTotal())
        printLatexHeader(os,totalr,"p{4.5cm}")
        doc.append(pylatex_utils.ltx_fin_reg + '\n')
        #ImprLtxLeyenda(doc)
        #doc.append(pylatex_utils.ltx_ampsnd
        doc.append(media_empty_line)
        ImprLtxLeyenda(doc)
        doc.append(pylatex_utils.ltx_fin_reg + '\n' + pylatex_utils.ltx_hline + '\n')
        quantities.ImprCompLtx(os)
        doc.append(media_empty_line)
        ImprLtxPie(os,totalr)
        doc.append(pylatex_utils.ltx_fin_reg + '\n')
        doc.append(pylatex_utils.ltx_hline + '\n')
        doc.add_empty_row()

    def getLtxBudgetRow(self, ancho):
        totalr=  basic_types.human_readable(self.getRoundedTotal())
        row= [pylatex_utils.ascii2latex(self.getUnitPriceCode())]
        row.append(totalr+ " " + pylatex_utils.ascii2latex(self.UnidadMedida()))
        row.append(pylatex.table.MultiColumn(1, align=pylatex.utils.NoEscape(ancho),data= self.ud.getNoEmptyDescription()))
        row.append(self.getUnitLtxPriceString())
        row.append(self.getLtxPriceString())
        return row

    def ImprCompLtxPre(self, data_table, other= None):
        data_table.add_empty_row()
        row= ['','', '', '', '']
        if(other):
            row= other.getLtxBudgetRow('p{2.5cm}')
        row.extend(self.getLtxBudgetRow("p{2.5cm}"))
        data_table.add_row(row)
        data_table.add_empty_row()

    def writePartialBudgetsIntoLatexDocument(self, data_table):
        row= self.getLtxBudgetRow('p{5cm}')
        data_table.add_row(row)
        data_table.add_empty_row()

    # Spreadsheet ouput.
    def writeSpreadsheetQuantities(self, sheet):
        ''' Write the quantities in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        '''
        sheet.append([self.getUnitPriceCode(), basic_types.human_readable(self.getTotal(),3), pylatex_utils.ascii2latex(self.UnidadMedida()), pylatex_utils.ascii2latex(self.ud.getNoEmptyDescription())])
        sheet.append(["Texto", "Unidades", "Largo", "Ancho", "Alto", "Parcial"])
        self.quantities.writeSpreadsheet(sheet)
        sheet.append([None,None,None,None,None,None])

    def writeSpreadsheetBudget(self, sheet):
        ''' Write the budget in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        '''
        sheet.append([self.getUnitPriceCode(), self.getTotal(),  self.UnidadMedida(),  self.ud.getNoEmptyDescription(), self.getUnitPriceString(), self.getPrice()])

    def WriteBC3RegM(self, os, cap_padre, pos):
        os.write("~M|" + cap_padre + '\\' + self.getUnitPriceCode() + '|'
           + str(pos) + '|'
           + str(self.getRoundedTotal()) + '|')

    def WriteBC3(self, os, cap_padre, pos):
        self.WriteBC3RegM(os,cap_padre,pos)
        self.quantities.WriteBC3(os)
        os.write('|' + '\n')

    @staticmethod
    def printLtxColumnHeaders(data_table):
        ''' Write the column headers in the given table.

        :param data_table: pylatex table to write into.
        '''
        data_table.add_row(["Texto","Unidades", "Largo", "Ancho","Alto","Parcial"])

    @staticmethod
    def ImprLtxPie(data_table, totalr):
        ''' Write the sum of the quantities in the given table.

        :param data_table: pylatex table to write into.
        :param totalr: total quantity to write in the table.
        '''
        data_table.add_row([pylatex.table.MultiColumn(5,align= 'r',data= pylatex.NoEscape("Suma\\ldots")),pylatex.utils.bold(totalr)])


    def writeQuantitiesIntoLatexDocument(self, data_table, superTabular= False):
        ''' Write the quantities in the given data table.

        :param data_table: pylatex table to write into.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        data_table.add_empty_row()
        totalr= basic_types.human_readable(self.getRoundedTotal())
        self.printLatexHeader(data_table,totalr,'p{6cm}')
        #data_table.append(pylatex_utils.ltx_fin_reg + '\n')
        self.printLtxColumnHeaders(data_table)
        data_table.add_hline()
        self.quantities.printLtx(data_table)
        self.ImprLtxPie(data_table,totalr)
        data_table.add_hline()
        data_table.add_empty_row()
        
    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(UnitPriceQuantitiesBase, self).getDict()
        retval['ud']= self.ud.Codigo()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= list() # Links that cannot be set yet.
        udCode= dct['ud']
        self.ud= None
        pendingLinks.append({'object':self, 'attr':'ud', 'key':udCode}) 
        pendingLinks.extend(super(UnitPriceQuantitiesBase, self).setFromDict(dct))
        return pendingLinks


