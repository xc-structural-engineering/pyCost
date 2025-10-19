# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

from pycost.utils import basic_types
from pycost.prices import elementary_price
from pycost.prices import unit_price
from pycost.structure import unit_price_quantities
from pycost.structure import chapter
from pycost.structure import obra

# Create root chapter.
site= obra.Obra(cod="test", tit="Test title")

# Create elementary prices.

sindesco= elementary_price.ElementaryPrice(cod='SINDESCO', tit= 'Sin descomposición', ud= 'ud', p= 1.0, tp= basic_types.sin_clasif, long_description= 'Iron worker')
site.precios.elementos.Append(sindesco) # Append elementary price.

# Create unit price.
oranges= unit_price.UnitPrice(cod="Oranges", desc="Oranges.", ud="kg", ld= "Oranges.")
## Append unit price components.
oranges.Append(entity= sindesco, f= 1.0, r= 1.78)
site.precios.unidades.Append(oranges)


# Measurements
## New chapter
ch01= site.newSubChapter(chapter.Chapter(cod= '01', tit= 'Oranges'))
## Orange quantities.
orangeMeasurements= unit_price_quantities.UnitPriceQuantities(site.getUnitPrice('Oranges'))
q1units= 2
q1l= 10.0
orangeMeasurements.appendMeasurement(textComment='test A', nUnits= q1units, length= q1l, width=None, height=None)
ch01.appendUnitPriceQuantities(orangeMeasurements)

cost= site.getPrice()
totalRefCost= 2*10*1.78
ratio1= abs(cost-totalRefCost)/totalRefCost

'''
print('cost= ', cost)
print('totalRefCost= ', totalRefCost)
print('ratio1= ', ratio1)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
