# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

import yaml
import pylatex
from pycost.structure import obra

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= "."
inputFile= open(pth+'/../data/bc3/test_file_10.bc3',mode='r', encoding="utf-8")

site.readBC3(inputFile)
inputFile.close()

# Write in YAML format
site.writeYaml(pth+'/../data/yaml/test_file_10.yaml')


# Get test values.
price= site.getPrice()
ratio1= abs(price-27.27)/27.27

# Get unit of the price EAS005
unit= site.findPrice('EAS005').Unidad()

'''
print('price: ', price)
print('ratio1: ', ratio1)
print('unit: ', unit)
doc=pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
# doc.append(pylatex.Command('doparttoc'))
site.writePartialBudgetsIntoLatexDocument(doc)
doc.generate_tex('partial_budgets')
'''

import os
import logging
fname= os.path.basename(__file__)
if ((ratio1<1e-6) and (unit=='Ud')):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
