# -*- coding: utf-8 -*-
#EntFR.py

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
