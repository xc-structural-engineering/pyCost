# -*- coding: utf-8 -*-
''' Entity that has a factor and production rate.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
from pycost.utils import basic_types
from pycost.utils import EntPyCost as epc
from decimal import Decimal

class EntFR(epc.EntPyCost):
    '''Entity that has a factor and production rate.'''
    precision= 3
    places= Decimal(10) ** -precision
    formatString= '{0:.'+str(precision)+'f}'

    def __init__(self, f= 1.0, r=0.0):
        super(EntFR, self).__init__()
        self.factor= f
        self.productionRate= r

    def getCopy(self):
        ''' Return a copy of this object.'''
        return EntFR(f= self.factor, r= self.productionRate)
    
    def getFactor(self):
        return self.factor

    def getProductionRate(self):
        return self.productionRate

    def getProduct(self):
        return self.factor*self.productionRate

    def getProductString(self):
        '''Return a string that represents the product.'''
        return self.formatString.format(self.getProduct())

    def getPercentageString(self):
        '''Return a string that represents the product as a percentage.'''
        return self.formatString.format(self.getProduct()*100)

    def getRoundedProduct(self):
        return Decimal(self.getProductString())

    def getRoundedPercentage(self):
        return Decimal(self.getPercentageString())

    def WriteSpre(self, os):
        os.write(self.getProductString() + '|')

    def WriteBC3(self, os):
        txtFactor=  self.formatString.format(self.factor)
        txtRate=  self.formatString.format(self.productionRate)
        os.write(txtFactor + '\\' + txtRate + '\\')

    def Write(self, os= sys.stdout):
        txtFactor=  self.formatString.format(self.factor)
        txtRate=  self.formatString.format(self.productionRate)
        os.write(' factor= '+txtFactor+ ' prod. rate: '+txtRate)
        

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(EntFR, self).getDict()
        retval['factor']= self.factor
        retval['production_rate']= self.productionRate
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary..

        :param dct: input dictionary.
        '''
        self.factor= dct['factor']
        self.productionRate= dct['production_rate']
        return super(EntFR, self).setFromDict(dct)
