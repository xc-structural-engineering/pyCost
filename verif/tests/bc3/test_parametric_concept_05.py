# -*- coding: utf-8 -*-
'''Check reading of parametric prices with matrix component values.''' 
from __future__ import division
from __future__ import print_function

from pycost.structure import obra
from pycost.structure import chapter
from pycost.structure import unit_price_quantities

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= "."
inputFile= open(pth+'/../data/bc3/test_parametric_05.bc3',mode='r')#, encoding="latin-1")

site.readBC3(inputFile)
inputFile.close()

# Get paramatric concept keys.
parametricConceptKeys= site.precios.unidades.getParametricConceptsKeys()
#print(parametricConceptKeys)

# Get the first parametric concept
pConcept= site.precios.unidades.getParametricConcept(key= parametricConceptKeys[0])

#print('parameterLabelLetters.keys=',pConcept.parameters.parameterLabelLetters.keys())
#print('parameterLabelStatements=',pConcept.parameters.parameterLabelStatements)
#Write the object parameters and its options.
#pConcept.writeParameterOptions()


# Write the object parameters and its options.
# pConcept.writeParameterOptions()
# Set the values for the optional parameters.
options= [('tipo','Casco de seguridad ajustable rueda')]

# Create unit price with the preceding options.
unitPrice= pConcept.getUnitPrice(code= parametricConceptKeys[0], options= options, rootChapter= site)

#unitPrice.Write()
# Append the price to the root chapter price table.
site.precios.unidades.Append(unitPrice)
# Measurements
## New chapter
ch01= site.newSubChapter(chapter.Chapter(cod= '01', tit= 'Chapter 01'))
## Quantities.
measurements= unit_price_quantities.UnitPriceQuantities(site.getUnitPrice(unitPrice.codigo))
measurements.appendMeasurement(textComment='test parametric price.', nUnits= 1, length= None, width=None, height=None)
ch01.appendUnitPriceQuantities(measurements)

# Check text substitutions.
texts= list()
for key in site.precios.unidades.concepts:
    ud= site.precios.unidades.concepts[key]
    texts.append(ud.title)
    texts.append(ud.long_description)

refTexts= ['Casco de seguridad ajustable rueda.', 'Casco de seguridad con arnés de cabeza ajustable por medio de rueda dentada, para uso normal y eléctrico hasta 440 V.. Según R.D. 773/97 y R.D. 1407/92. Equipo de Protección Individual (EPI) con marcado de conformidad CE.']
textsOK= (texts==refTexts)

# Compute cost.
cost= site.getPrice()
totalRefCost= 11.20
ratio1= abs(cost-totalRefCost)/totalRefCost

'''
print(texts)
print('cost= ', cost)
print('ratio1= ', ratio1)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-2) and textsOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
