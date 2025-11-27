# -*- coding: utf-8 -*-
''' Quantities report.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
from pycost.prices import unit_price_report
from pycost.utils import basic_types
from pycost.utils import pylatex_utils
from operator import itemgetter

class QuantitiesReport(dict):

    def Inserta(self, iu):
        ''' Inserts a unit price in the report.'''
        uPrice= iu.Unidad()
        if(uPrice in self):
            self[uPrice]+= iu.Medicion() # Add to the existing record.
        else:
            (self)[uPrice]= iu.Medicion() # Create new record.

    def Merge(self, otro):
        for key in otro:
            value= otro[key]
            self.Inserta(unit_price_report.UnitPriceReport(key,value))

    def getKeysWithMeasurementGreaterThan(self, lowerMeasurementBound):
        ''' Return the codes of the prices that have a total measurement
            greater than the limit argument.

        :param lowerMeasurementBound: lower bound for the total measurement.
        '''
        retval= set()
        for key in self:
            totalMeasurement= self[key]
            if(totalMeasurement>lowerMeasurementBound):
                code= key.Codigo()
                retval.add(code)
        return retval

    def getElementaryQuantities(self):
        ''' Return the quantities corresponding to each of the elementary prices
            present in the concepts of this container.
        '''
        retval= dict()
        for price in self:
            quantity= self[price]
            if(price.isCompound()): # compound price.
                parentPrices= [price.Codigo()]
                elementaryComponents= price.getElementaryComponents(parentPrices= parentPrices)
                for code in elementaryComponents:
                    ec= elementaryComponents[code]
                    c_code= ec.CodigoEntidad()
                    c_quantity= ec.getProduct()*quantity
                    if(c_code in retval):
                        retval[c_code]+= c_quantity
                    else:
                        retval[c_code]= c_quantity
                parentPrices.pop()
            else: # elementary price.
                code= price.Codigo()
                if(code in retval):
                    retval[code]+= quantity
                else:
                    retval[code]= quantity
        return retval

    def getRows(self, currencySymbol, biggestAmountFirst= True, limitTextWidth= None):
        ''' Return the report in a Python list. For each record in this 
        containe return a row containing the  price code, its descritipion, 
        the quantity employed and the price of that quantity.

        :param biggestAmountFirst: if true sort the list from the biggest to the
                                   smallest amount of money.
        :param currencySymbol: symbol of the currency.
        :param limitTextWidth: maximum length of the returned description. 
        '''
        retval= list()
        for unitPrice in self:
            quantity= self[unitPrice]
            title= unitPrice.title
            if(limitTextWidth):
                if(len(title)>limitTextWidth):
                    limit= limitTextWidth-3
                    title= title[0:limit]+'...'
            unit= basic_types.fix_unit_text(unitPrice.unidad)
            price= float(unitPrice.getPrice())*quantity
            code= unitPrice.Codigo()
            retval.append([code, title, quantity, unit, price, currencySymbol])
        if(biggestAmountFirst):
            retval= list(reversed(sorted(retval, key=itemgetter(4))))
        return retval

    def printLtx(self, doc, superTabular= False):
        ''' Write Latex report.

        :param doc: pylatex document to write into.
        :param superTabular: if true, use supertabular instead of longtable.
        '''
        sz= len(self)
        if(sz>0):
            doc.append(pylatex_utils.SmallCommand())
            longTableStr= '|l|p{6cm}|r|r|'
            headerRow= [u"Código",u"Descripción.",u"Medición",'Precio']
            num_fields= 4
            if(superTabular):
                # Create LaTeX supertabular.
                ## Remove/redefine previous heads and tails.
                head_str= '\\hline%\n'+'&'.join(headerRow)+'\\\\%\n\\hline%\n'
                pylatex_utils.supertabular_first_head(doc, firstHeadStr= head_str)
                pylatex_utils.supertabular_head(doc, headStr= head_str)
                superTabularTailStr= '\\hline%\n\\multicolumn{'+str(num_fields)+'}{|r|}{../..}\\\\%\n\\hline%\n'
                pylatex_utils.supertabular_tail(doc, tailStr= superTabularTailStr)
                pylatex_utils.supertabular_last_tail(doc, lastTailStr= '\\hline%\n')
                with doc.create(pylatex_utils.SuperTabular(longTableStr)) as data_table:
                    pass

            else:
                # Create LaTeX longtable.
                with doc.create(pylatex.table.LongTable(longTableStr)) as data_table:
                    data_table.add_hline()
                    data_table.add_row(headerRow)
                    data_table.add_hline()
                    data_table.end_table_header()
                    data_table.add_hline()
                    data_table.add_row((pylatex.table.MultiColumn(num_fields,
                                                                  align='|r|',
                                                                  data='../..'),))
                    data_table.add_hline()
                    data_table.end_table_footer()
                    data_table.add_hline()
                    data_table.end_table_last_footer()

            for key in self:
                value= self[key]
                iu= unit_price_report.UnitPriceReport(key,value)
                iu.printLtx(data_table)
            doc.append(pylatex_utils.NormalSizeCommand())

def get_rows_elementary_quantities(elementaryQuantitiesDict, currencySymbol, biggestAmountFirst= True, limitTextWidth= None):
    ''' For each record in the given dictionary return a row containing the 
        elementary price code, its descritipion, the quantity employed and
        the price of that quantity.


        :param elementaryQuantitiesDict: dictionary containing the quantities
                                         of each elementary price.
        :param biggestAmountFirst: if true sort the list from the biggest to the
                                   smallest amount of money.
        :param currencySymbol: symbol of the currency. 
        :param limitTextWidth: maximum length of the returned description. 
    '''
    retval= list()
    for elementaryPrice in elementaryQuantitiesDict:
        quantity= elementaryQuantitiesDict[elementaryPrice]
        title= elementaryPrice.title
        if(limitTextWidth):
            if(len(title)>limitTextWidth):
                limit= limitTextWidth-3
                title= title[0:limit]+'...'
        unit= basic_types.fix_unit_text(elementaryPrice.unidad)
        price= float(elementaryPrice.getPrice())*quantity
        code= elementaryPrice.Codigo()
        retval.append([code, title, quantity, unit, price, currencySymbol])
    if(biggestAmountFirst):
        retval= list(reversed(sorted(retval, key=itemgetter(4))))
    return retval
