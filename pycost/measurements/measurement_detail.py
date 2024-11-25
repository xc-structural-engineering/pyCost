# -*- coding: utf-8 -*-
''' Measurement detail.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
from pycost.utils import EntPyCost as epy
from pycost.measurements import measurement_record
from pycost.utils import basic_types
from pycost.utils import pylatex_utils

class Quantities(list, epy.EntPyCost):
    '''Quantities de una unidad de obra.'''

    def __init__(self):
        ''' Constructor.'''
        super(Quantities, self).__init__()
        epy.EntPyCost.__init__(self)
            
    def getTotalUnits(self):
        '''Return the total number of units.'''
        t= measurement_record.MeasurementRecord.dimension(0.0)
        for i in self:
            t+=(i).Unidades()
        return t

    def getTotalLength(self):
        '''Return the total length.'''
        t= measurement_record.MeasurementRecord.dimension(0.0)
        for i in self:
            t+=(i).Unidades()*(i).Largo()
        return t

    def getTotalWidth(self):
        '''Return the total width.'''
        t= measurement_record.MeasurementRecord.dimension(0.0)
        for i in self:
            t+=(i).Unidades()*(i).Ancho()
        return t

    def getTotalHeight(self):
        '''Return the total height.'''
        t= measurement_record.MeasurementRecord.dimension(0.0)
        for i in self:
            t+=(i).Unidades()*(i).Ancho()
        return t

    def getTotal(self):
        t= 0.0
        for i in self:
            t+=(i).getTotal()
        return t

    def getRoundedTotal(self):
        t= measurement_record.MeasurementRecord.dimension(0.0)
        for i in self:
            t+=(i).getRoundedTotal()
        return t

    def readBC3(self, m):
        ''' Read quantities list.'''
        for l in m:
            rm= measurement_record.MeasurementRecord()
            rm.readBC3(l)
            self.append(rm)

    def WriteBC3(self, os):
        for i in self:
            (i).WriteBC3(os)

    def ImprCompLtx(self, doc, otra):
        ''' Write LaTeX report.

        :param doc: pylatex document to write into.
        '''
        media_empty_line= ['','', '', '', '']
        for i in self:
          for j in otra:
            (j).printLtx(os,"p{1.5cm}")
            doc.append(pylatex_utils.ltx_ampsnd)
            (i).printLtx(os,"p{1.5cm}")
            doc.append(pylatex_utils.ltx_fin_reg + '\n')

        # if i:
        #     for(; i!=end(); i+= 1)
        #         doc.append(media_empty_line
        #         doc.append(pylatex_utils.ltx_ampsnd)
        #         (i).printLtx(os,"p{1.5cm}")
        #         doc.append(pylatex_utils.ltx_fin_reg + '\n')

        # elif j!=end():
        #     for(; j!=otra.end(); j+= 1)
        #         (j).printLtx(os,"p{1.5cm}")
        #         doc.append(media_empty_line + pylatex_utils.ltx_fin_reg + '\n'

        doc.add_empty_row()

    def ImprCompLtx(self, doc):
        ''' Write LaTeX report.

        :param doc: pylatex document to write into.
        '''
        media_empty_line= ['','', '', '', '', '']
        for i in self:
            doc.append(media_empty_line)
            (i).printLtx(os,"p{1.5cm}")
            doc.append(pylatex_utils.ltx_fin_reg + '\n')
        doc.add_empty_row()

    def printLtx(self, data_table):
        for i in self:
            (i).printLtx(data_table,"p{3.5cm}")
        data_table.add_empty_row()

    def writeSpreadsheet(self, sheet):
        ''' Write the quantities in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        '''
        for i in self:
            (i).writeSpreadsheet(sheet)
        sheet.append([None,None,None,None,'Suma ...',self.getTotal()])
        sheet.append([])

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= epy.EntPyCost.getDict(self)
        for idx, i in enumerate(self):
            retval[idx]= i.getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.'''
        pendingLinks= list() # Links that cannot be set yet.
        for key in dct:
            itemDict= dct[key]
            item= measurement_record.MeasurementRecord()
            pendingLinks.extend(item.setFromDict(itemDict))
            self.append(item)
        pendingLinks.extend(epy.EntPyCost.setFromDict(self,dct))
        return pendingLinks
