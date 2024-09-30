# -*- coding: utf-8 -*-
''' Base class for measurable objects.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pycost.structure import unit_price_quantities

def gen_quantities(currentChapter, cod, lst_med):
    ''' Generates the cuantities from the given list.

    :param currentChapter: chapter to add the quantities to.
    :param cod: price corresponding to the measured quantities.
    :param lst_med: list of measurements.
    ''' 
    rootChapter= currentChapter.getRootChapter()
    currentPrice= rootChapter.getUnitPrice(cod)
    currentQuantities= unit_price_quantities.UnitPriceQuantities(currentPrice)
    for lmed in lst_med:
        txt= lmed[0]
        ud= lmed[1]
        largo= lmed[2]
        ancho= lmed[3]
        alto= lmed[4]
        currentQuantities.appendMeasurement(txt,ud,largo,ancho,alto)
    currentChapter.appendUnitPriceQuantities(currentQuantities)
    
