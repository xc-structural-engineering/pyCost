# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

import json
from pycost.structure import obra
from pycost.structure import chapter
from pycost.structure import unit_price_quantities

# Create main object.
oldSite= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= "."
inputFile= open(pth+'/../data/bc3/test_parametric_01.bc3',mode='r')
oldSite.readBC3(inputFile)
inputFile.close()

siteCost= oldSite.getPrice()

# Dump into json file.
jsonFileName= pth+'/../data/json/test_parametric_01.json'
oldSite.writeJson(jsonFileName)

# Read from json file
newSite= obra.Obra(cod="newSite", tit="New site")
pendingLinks= newSite.readFromJson(jsonFileName)

# Get parametric concept keys.
parametricConceptKeys= newSite.precios.unidades.getParametricConceptsKeys()

# Get the first parametric concept
pConcept= newSite.precios.unidades.getParametricConcept(key= parametricConceptKeys[0])

# # Write the object parameters and its options.
# pConcept.writeParameterOptions()

# Set the values for the optional parameters.
options= [('altura_de_apeo', '<6 m'), ('condiciones_de_ejecución', 'Volumen escaso'), ('trabajo', 'Diurno'), ('banda_de_mantenimiento', 'i<3 horas')]

# Create unit price with the preceding options.
unitPrice= pConcept.getUnitPrice(code= parametricConceptKeys[0], options= options, rootChapter= newSite)

# Append the price to the root chapter price table.
newSite.precios.unidades.Append(unitPrice)

# Measurements
## New chapter
ch01= newSite.newSubChapter(chapter.Chapter(cod= '01', tit= 'Chapter 01'))
## Quantities.
measurements= unit_price_quantities.UnitPriceQuantities(newSite.getUnitPrice(unitPrice.codigo))
measurements.appendMeasurement(textComment='test parametric price.', nUnits= 4, length= 2, width=12, height=None)
ch01.appendUnitPriceQuantities(measurements)

# Compute cost.
cost= newSite.getPrice()
totalRefCost= 7237.4400000000005
ratio1= abs(cost-totalRefCost)/totalRefCost

'''
print(parametricConceptKeys)
print('cost= ', cost)
print('ratio1= ', ratio1)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
