# -*- coding: utf-8 -*-
''' Unit price quantities.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pycost.structure import unit_price_quantities_base as ptp
from pycost.measurements import measurement_detail as m
from pycost.measurements import measurement_record as mr

class UnitPriceQuantities(ptp.UnitPriceQuantitiesBase):
    '''UnitPriceQuantities del presupuesto correspondiente 
       a una unidad de obra.'''

    def __init__(self, u= None):
        super(UnitPriceQuantities,self).__init__(u)
        self.quantities= m.Quantities()

    def getTotal(self):
        return self.quantities.getTotal()

    def getRoundedTotal(self):
        return self.quantities.getRoundedTotal()

    def readBC3(self, m):
        ''' Read quantities from BC3 record.'''
        empty= len(m.med.lista_med.lines)==0
        if(empty):
            rm= mr.MeasurementRecord("",m.med.med_total)
            self.quantities.append(rm)
        else:
            self.quantities.readBC3(m.med.lista_med.lines)

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(UnitPriceQuantities, self).getDict()
        retval['measurements']= self.quantities.getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= self.quantities.setFromDict(dct['measurements']) # Links that cannot be set yet.
        pendingLinks.extend(super(UnitPriceQuantities, self).setFromDict(dct))
        return pendingLinks
    
    def clear(self):
        '''removes all items from the chapter.'''
        self.quantities.clear()

    def appendMeasurement(self, textComment,nUnits,length,width,height):
        '''Add generic quantities to the price defined as parameter

        :param textComment:   string to comment each measuremt line generated 
        :param nUnits: number of units
        :param length, width, height: dimensions
        '''
        self.quantities.append(mr.MeasurementRecord(textComment,nUnits, length, width, height))

