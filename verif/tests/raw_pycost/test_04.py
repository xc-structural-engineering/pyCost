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
threePercent= elementary_price.ElementaryPrice(cod= '%003', tit= "3 % Medios auxiliares", ud="%", p=0.0, tp= basic_types.sin_clasif, long_description= "3 % Medios auxiliares")
site.precios.elementos.Append(threePercent) # Append elementary price.

oficFer= elementary_price.ElementaryPrice(cod='OFICFER', tit= 'Iron worker', ud= 'h', p= 18.14, tp= basic_types.mdo, long_description= 'Iron worker')
site.precios.elementos.Append(oficFer) # Append elementary price.

peon= elementary_price.ElementaryPrice(cod='PEONES', tit= 'Specialized laborer', ud= 'h', p= 13.75, tp= basic_types.mdo, long_description= 'Specialized laborer')
site.precios.elementos.Append(peon) # Append elementary price.

steel= elementary_price.ElementaryPrice(cod='MAACE0201', tit= 'Rebar steel', ud= 'kg', p= 0.62, tp= basic_types.mat, long_description= 'Rebar steel')
site.precios.elementos.Append(steel) # Append elementary price.


# Create unit price.
reinforcingSteel= unit_price.UnitPrice(cod="ACERO0103", desc="Reinforcement steel.", ud="kg", ld= "Reinforcement steel.")
## Append unit price components.
reinforcingSteel.Append(entity= oficFer, f= 1.0, r= .015)
reinforcingSteel.Append(entity= peon, f= 1.0, r= .015)
reinforcingSteel.Append(entity= steel, f= 1.0, r= 1.0)
reinforcingSteel.Append(entity= threePercent, f= 1.0, r= .03)
site.precios.unidades.Append(reinforcingSteel)


# Measurements
## New chapter
ch01= site.newSubChapter(chapter.Chapter(cod= '01', tit= 'Chapter 01'))
## MAACE0201 quantities.
rebarMeasurements= unit_price_quantities.UnitPriceQuantities(site.getUnitPrice('MAACE0201'))
q1units= 2
q1l= 10.0
rebarMeasurements.appendMeasurement(textComment='test A', nUnits= q1units, length= q1l, width=None, height=None)
ch01.appendUnitPriceQuantities(rebarMeasurements)

## ACERO0103 quantities.
reinfMeasurements= unit_price_quantities.UnitPriceQuantities(site.getUnitPrice('ACERO0103'))
q2units= 20
q2l= 25.0
reinfMeasurements.appendMeasurement(textComment='test B', nUnits= q2units, length= q2l, width=None, height=None)
ch01.appendUnitPriceQuantities(reinfMeasurements)

cost= site.getPrice()
totalRefCost= 577.4
ratio1= abs(cost-totalRefCost)/totalRefCost

'''
print('ratio1= ', ratio1)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
