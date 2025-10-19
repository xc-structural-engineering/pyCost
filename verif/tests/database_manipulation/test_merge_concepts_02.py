# -*- coding: utf-8 -*-
'''Merge two price databases.''' 
from __future__ import division
from __future__ import print_function

import yaml
import pickle
from pycost.structure import obra
from pycost.structure.chapter import Chapter
from pycost.structure.unit_price_quantities import UnitPriceQuantities

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'

# Read price data from two databases
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_03_prices.yaml')
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_file_07.yaml')

ch01= site.newSubChapter(Chapter(cod= '01', tit= 'Chapter 01'))

# Measurements
## MAACE0201 quantities.
rebarMeasurements= UnitPriceQuantities(site.getUnitPrice('MAACE0201'))
q1units= 2
q1l= 10.0
rebarMeasurements.appendMeasurement(textComment='test A', nUnits= q1units, length= q1l, width=None, height=None)
ch01.appendUnitPriceQuantities(rebarMeasurements)
## SAA010b quantities.
testMeasurements= UnitPriceQuantities(site.getUnitPrice('SAA010b'))
testMeasurements.appendMeasurement(textComment='test B', nUnits= 1, length= 2, width=3, height=4)
ch01.appendUnitPriceQuantities(testMeasurements)

# Compute costs
q1Cost= rebarMeasurements.getPrice()
refQ1Cost= rebarMeasurements.getUnitPrice()*q1units*q1l
ratio1= abs(q1Cost-refQ1Cost)/refQ1Cost

q2Cost= testMeasurements.getPrice()
refQ2Cost= float(testMeasurements.getUnitPrice())*24
ratio1= abs(q2Cost-refQ2Cost)/refQ2Cost

totalRefCost= refQ1Cost+refQ2Cost

cCost= ch01.getPrice()
ratio2= abs(cCost-totalRefCost)/totalRefCost

cost= site.getPrice()
ratio3= abs(cost-totalRefCost)/totalRefCost

'''
print('rebar measurements cost: ', q1Cost)
print('rebar reference cost: ', refQ1Cost)
print('ratio1= ', ratio1)
print('chapter cost: ', cCost)
print('ratio2= ', ratio2)
print('total cost: ', cost)
print('ratio3= ', ratio3)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6) and (ratio2<1e-6) and (ratio3<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
