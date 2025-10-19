# -*- coding: utf-8 -*-
'''Trivial PyCost test.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2022, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pycost.structure import obra
from pycost.structure import chapter
from pycost.structure import unit_price_quantities

# Create main object.
rootChapter= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= "."
inputFile= open(pth+'/../data/bc3/test_file_06.bc3',mode='r', encoding="latin-1")

rootChapter.readBC3(inputFile)
inputFile.close()

# Write in JSON format
rootChapter.writeJson(pth+'/../data/json/test_file_08.json')

# Measurements
## New chapter
ch01= rootChapter.newSubChapter(chapter.Chapter(cod= '01', tit= 'Chapter 01'))
## EAS010 quantities.
steelMeasurements= unit_price_quantities.UnitPriceQuantities(rootChapter.getUnitPrice('EAS010'))
steelMeasurements.appendMeasurement(textComment='test A', nUnits= 26, length= 10, width=51.2, height=None)
ch01.appendUnitPriceQuantities(steelMeasurements)

# Get test values.
price= rootChapter.getPrice()
numChapters= len(rootChapter.subcapitulos)
refPrice= 28487.68
ratio= abs(price-refPrice)/refPrice

'''
print('price: ', price)
for ch in rootChapter.subcapitulos:
    print(ch.Codigo(), ch.title)
print('num chapters: ', numChapters)
'''

import os
import logging
fname= os.path.basename(__file__)
if ((ratio<1e-6) and (numChapters==2)):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
