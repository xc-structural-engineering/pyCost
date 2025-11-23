# -*- coding: utf-8 -*-
''' Unit price report.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pycost.utils import pylatex_utils
from pycost.utils import basic_types


class UnitPriceReport(object):
    ''' Data to report the quantity corresponding to a unit price.

    :ivar ud: unit to which the quantity corresponds.
    ;ivar med_total: measured quantity.
    '''
    def __init__(self, u, mt):
        ''' Constructor.

        :param ud: unit to which the quantity corresponds.
        ;param med_total: measured quantity.
        '''
        self.ud= u
        self.med_total= mt
        
    def Unidad(self):
        ''' Return the unit price.'''
        return self.ud
    
    def Medicion(self):
        ''' Return the measured quantity.'''
        return self.med_total
    
    def printLtx(self, data_table):
        ''' Fills the given LaTeX table with the data of this objeect.

        :param data_table: pylatex table to write into.
        '''
        precision= 2
        if self.ud:
            row= [self.ud.Codigo()]
            row.append(pylatex_utils.ascii2latex(self.ud.getNoEmptyDescription()))
            row.append(basic_types.human_readable(self.med_total,precision))
            row.append(basic_types.human_readable(self.med_total*float(self.ud.getPrice()),precision))
            data_table.add_row(row)


