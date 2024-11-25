# -*- coding: utf-8 -*-
''' Measurement record.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
import decimal
from pycost.prices import unit_price
from pycost.utils import basic_types
from pycost.utils import EntPyCost as epc
from pycost.utils import pylatex_utils

class MeasurementRecord(epc.EntPyCost):
    precision= 3
    places= decimal.Decimal(10) ** -precision
    formatString= '{0:.'+str(precision)+'f}'

    @staticmethod
    def dimension(dim):
        return decimal.Decimal(MeasurementRecord.formatString.format(dim))

    def __init__(self,c= "", uds= None,l= None,an= None,al= None):
        super(MeasurementRecord,self).__init__()
        self.comentario= c #unicode(c,encoding='utf-8')
        self.unidades= uds
        self.largo= l
        self.ancho= an
        self.alto= al

    def Comentario(self):
        return self.comentario

    def Unidades(self):
        return self.unidades

    def Largo(self):
        return self.largo

    def Ancho(self):
        return self.ancho

    def Alto(self):
        return self.alto
    
    def getUnitsString(self):
        retval= ''
        if(self.unidades):
            retval= self.formatString.format(self.unidades)
        return retval

    def getLengthString(self):
        retval= ''
        if(self.largo):
            retval= self.formatString.format(self.largo)
        return retval

    def getWidthString(self):
        retval= ''
        if(self.ancho):
            retval= self.formatString.format(self.ancho)
        return retval

    def getHeightString(self):
        retval= ''
        if(self.alto):
            retval= self.formatString.format(self.alto)
        return retval

    def UnidadesR(self):
        retval= None
        if(self.unidades):
            retval= decimal.Decimal(self.getUnitsString())
        return retval

    def LargoR(self):
        retval= None
        if(self.largo):
            retval= decimal.Decimal(self.getLengthString())
        return retval

    def AnchoR(self):
        retval= None
        if(self.ancho):
            retval= decimal.Decimal(self.getWidthString())
        return retval

    def AltoR(self):
        retval= None
        if(self.alto):
            retval= decimal.Decimal(self.getHeightString())
        return retval

    def isNull(self):
        '''Returns true if the measurement result is zero.'''
        retval= False
        if(self.unidades==0.0) and (self.largo==0.0) and (self.ancho==0.0) and (self.alto==0.0):
            retval= True
        else:
            if(self.unidades==None) and (self.largo==None) and (self.ancho==None) and (self.alto==None):
                retval= True
        return retval

    def getTotal(self):
        retval= 0.0
        if(not self.isNull()):
            retval= 1.0
            if(self.unidades): retval*= self.unidades
            if(self.largo): retval*= self.largo
            if(self.ancho): retval*= self.ancho
            if(self.alto): retval*= self.alto
        return retval


    def getRoundedTotal(self):
        retval= self.dimension(0.0)
        if(not self.isNull()):
            u= self.UnidadesR()
            l= self.LargoR()
            a= self.AnchoR()
            h= self.AltoR()
            tmp= self.dimension(1.0)
            if(u): tmp*= u
            if(l): tmp*= l
            if(a): tmp*= a
            if(h): tmp*= h
            retval= tmp.quantize(self.places, rounding=decimal.ROUND_HALF_UP)
        return retval

    def readBC3(self, m):
        ''' Read measurement.'''
        self.comentario= m['comentario']
        self.unidades= m['unidades']
        self.largo= m['largo']
        self.ancho= m['ancho']
        self.alto= m['alto']

    def getComponents(self):
        '''Return measurement components: 
           [description,number of units, length, width and height].'''
        retval= [ self.comentario, '','','','']
        if(self.unidades): retval[1]= self.getUnitsString()
        if(self.largo): retval[2]= self.getLengthString()
        if(self.ancho): retval[3]= self.getWidthString()
        if(self.alto): retval[4]= self.getHeightString()
        return retval
    
    def WriteBC3(self, os):
        components= self.getComponents()
        os.write('\\' + components[0] + '\\'
           + components[1] + '\\'
           + components[2] + '\\'
           + components[3] + '\\'
           + components[4] + '\\')

    def Write(self, os):
        os.write(self.comentario + ','
           + self.unidades + ','
           + str(self.largo) + ',' + str(self.ancho) + ',' + str(self.alto) + '\n')
    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(MeasurementRecord, self).getDict()
        retval['commentary']= self.comentario
        retval['units']= self.unidades
        retval['width']= self.ancho
        retval['length']= self.largo
        retval['height']= self.alto
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        self.comentario= dct['commentary']
        self.unidades= dct['units']
        self.largo= dct['length']
        self.ancho= dct['width']
        self.alto= dct['height']
        return super(MeasurementRecord, self).setFromDict(dct)

    #not  @brief Imprime la medición en Latex.
    def printLtx(self, data_table, ancho):
        row= [pylatex.table.MultiColumn(1,align= pylatex.utils.NoEscape(ancho),data= pylatex_utils.ascii2latex(self.comentario))]
        components= self.getComponents()
        zero= self.dimension(0.0);
        row.append(components[1])
        row.append(components[2])
        row.append(components[3])
        row.append(components[4])
        total= self.getRoundedTotal()
        if(total!=zero):
            str_t= basic_types.human_readable(total)
        else:
            str_t= ''
        row.append(str_t)
        data_table.add_row(row)

    def writeSpreadsheet(self, sheet):
        ''' Write the quantities in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        '''
        row= [self.comentario]
        if(self.unidades!=0.0):
            row.append(self.unidades)
        else:
            row.append(None)
        if(self.largo!=0.0):
            row.append(self.largo)
        else:
            row.append(None)
        if(self.ancho!=0.0):
            row.append(self.ancho)
        else:
            row.append(None)
        if(self.alto!=0.0):
            row.append(self.alto)
        else:
            row.append(None)
        total= self.getTotal()
        if(total!=0.0):
            row.append(total)
        else:
            row.append(None)
        sheet.append(row)

