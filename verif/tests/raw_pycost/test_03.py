# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

import os
from pycost.structure import obra
from pycost.structure.chapter import Chapter
from pycost.structure.unit_price_quantities import UnitPriceQuantities

obra= obra.Obra(cod="test", tit="Test title")

# Read data from file.
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
obra.readFromYaml(pth+'/../data/yaml/test_03_prices.yaml')

ch01= obra.newSubChapter(Chapter(cod= '01', tit= 'Chapter 01'))

# Measurements
## MAACE0201 quantities.
rebarMeasurements= UnitPriceQuantities(obra.getUnitPrice('MAACE0201'))
q1units= 2
q1l= 10.0
rebarMeasurements.appendMeasurement(textComment='test A', nUnits= q1units, length= q1l, width=None, height=None)
ch01.appendUnitPriceQuantities(rebarMeasurements)

## ACERO0103 quantities.
reinfMeasurements= UnitPriceQuantities(obra.getUnitPrice('ACERO0103'))
q2units= 20
q2l= 25.0
reinfMeasurements.appendMeasurement(textComment='test B', nUnits= q2units, length= q2l, width=None, height=None)
ch01.appendUnitPriceQuantities(reinfMeasurements)

q1Cost= rebarMeasurements.getPrice()
refQ1Cost= rebarMeasurements.getUnitPrice()*q1units*q1l
ratio1= abs(q1Cost-refQ1Cost)/refQ1Cost

q2Cost= reinfMeasurements.getPrice()
refQ2Cost= float(reinfMeasurements.getUnitPrice())*q2units*q2l
ratio2= abs(q2Cost-refQ2Cost)/refQ2Cost

totalRefCost= refQ1Cost+refQ2Cost

cCost= ch01.getPrice()
ratio3= abs(cCost-totalRefCost)/totalRefCost

cost= obra.getPrice()
ratio4= abs(cost-totalRefCost)/totalRefCost

'''
print('rebar measurements cost: ', q1Cost)
print('rebar reference cost: ', refQ1Cost)
print('ratio1= ', ratio1)
print('reinf measurements cost: ', q2Cost)
print('reinf reference cost: ', refQ2Cost)
print('ratio2= ', ratio2)
print('chapter cost: ', cCost)
print('ratio3= ', ratio3)
print('total cost: ', cost)
print('ratio4= ', ratio4)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6) and (ratio2<1e-6) and (ratio3<1e-6) and (ratio4<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
