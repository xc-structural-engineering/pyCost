# -*- coding: utf-8 -*-
'''Read price database.''' 
from __future__ import division
from __future__ import print_function

from pycost.structure import obra
from pycost.structure import unit_price_quantities
from pycost.structure import chapter

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= "."
inputFile= open(pth+'/../data/bc3/test_parametric_01.bc3',mode='r')
site.readBC3(inputFile)
inputFile.close()

# Get paramatric concept keys.
parametricConceptKeys= site.precios.unidades.getParametricConceptsKeys()

# Get the first parametric concept
pConcept= site.precios.unidades.getParametricConcept(key= parametricConceptKeys[0])

# print('parameterLabelLetters.keys=',pConcept.parameters.parameterLabelLetters.keys())
# print('parameterLabelStatements=',pConcept.parameters.parameterLabelStatements)
# # Write the object parameters and its options.
#pConcept.writeParameterOptions()

# Set the values for the optional parameters.
options= [('altura_de_apeo', '<6 m'), ('condiciones_de_ejecución', 'Volumen escaso'), ('trabajo', 'Diurno'), ('banda_de_mantenimiento', 'i<3 horas')]

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
measurements.appendMeasurement(textComment='test parametric price.', nUnits= 4, length= 2, width=12, height=None)
ch01.appendUnitPriceQuantities(measurements)

# Check text substitutions.
texts= list()
for key in site.precios.unidades.concepts:
    ud= site.precios.unidades.concepts[key]
    texts.append(ud.title)
    texts.append(ud.long_description)
refTexts= ['Apeo de estructuras c/metal <6 m. (D/<3/E)', 'Apeo de estructura, hasta una altura máxima de 6 m, mediante sopandas, puntales y durmientes metálicos, con parte proporcional de medios auxiliares y trabajos previos de limpieza para apoyos. Medida superficie realmente apeada descontando huecos. Según normativa de aplicación nacional y/o equivalente europea. Trabajo: Diurno. Banda de mantenimiento: i<3 horas. Condiciones de ejecución: Volumen escaso.']
textsOK= (texts==refTexts)

# Compute cost.
cost= site.getPrice()
totalRefCost= 7237.4400000000005
ratio1= abs(cost-totalRefCost)/totalRefCost

'''
print(texts)
print('cost= ', cost)
print('ratio1= ', ratio1)
'''

import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6) and textsOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
