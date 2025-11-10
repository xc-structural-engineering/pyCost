# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

import math
import yaml
import pylatex
from pycost.structure import obra

# Create main object.
rootChapter= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= "."
inputFile= open(pth+'/../data/bc3/test_file_11.bc3', mode='r', encoding= 'cp850')

rootChapter.readBC3(inputFile)
inputFile.close()

gag030= rootChapter.findPrice('GAG030')
priceGAG030= float(gag030.getPrice())
cm1u00u020= rootChapter.findPrice('CM1U00U020')
priceCM1U00U020= float(cm1u00u020.getPrice())
cm1u00u070= rootChapter.findPrice('CM1U00U070')
priceCM1U00U070= float(cm1u00u070.getPrice())
cm1u01aof010= rootChapter.findPrice('CM1U01AOF010')
priceCM1U01AOF010= float(cm1u01aof010.getPrice())
cm1e03mh010= rootChapter.findPrice('CM1E03MH010')
priceCM1E03MH010= float(cm1e03mh010.getPrice())

# Get test values.
err= (priceGAG030-34.14)**2
err+= (priceCM1U00U020-12.81)**2
err+= (priceCM1U00U070-6.48)**2
err+= (priceCM1U01AOF010-4.10)**2
err+= (priceCM1E03MH010-916.88)**2


err= math.sqrt(err)


'''
print(priceGAG030)
print(priceCM1U00U020)
print(priceCM1U00U070)
print(priceCM1U01AOF010)
print(priceCM1E03MH010)
doc=pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
# doc.append(pylatex.Command('doparttoc'))
rootChapter.writePartialBudgetsIntoLatexDocument(doc)
doc.generate_tex('partial_budgets')
rootChapter.writePriceJustification(doc)
doc.generate_tex('price_justification')
'''

import os
import logging
fname= os.path.basename(__file__)
if (err<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')

