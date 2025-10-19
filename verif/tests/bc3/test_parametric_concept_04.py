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
inputFile= open(pth+'/../data/bc3/test_parametric_04.bc3',mode='r')#, encoding="latin-1")

site.readBC3(inputFile)
inputFile.close()


# Get paramatric concept keys.
parametricConceptKeys= site.precios.unidades.getParametricConceptsKeys()
#print(parametricConceptKeys)

# Get the first parametric concept
pConcept= site.precios.unidades.getParametricConcept(key= parametricConceptKeys[0])

#print('parameterLabelLetters.keys=',pConcept.parameters.parameterLabelLetters.keys())
#print('parameterLabelStatements=',pConcept.parameters.parameterLabelStatements)
# Write the object parameters and its options.
#pConcept.writeParameterOptions()


# Set the values for the optional parameters.
options= [('operación','Suministro, montaje y puesta en servicio'), ('edificio_de_control', 'subestación'), ('disposición', 'adosada a REE'), ('router_-_switch', '1 Gbit/s - 100 Mbit/s'), ('trabajo-corte_de_tensión','nocturno, con corte de tensión')]

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
refTexts= [' Suministro, montaje y puesta en servicio arquitectura de comunicaciones routers y switches 1 Gbit/s - 100 Mbit/s en subestación. Con corte de tensión. (N/-/-). ', ' Suministro, montaje y puesta en servicio de arquitectura de SICD, Suministro, montaje y puesta en servicio de routers y switches 1 Gbit/s - 100 Mbit/s e instalación , tendido y conexionado de switches  y routers con el cable de fibra óptica en subestación adosada a REE según condiciones técnicas del sistema integrado de control distribuido en subestaciones y centros de autotransformación, u otro documento similar, en vigor. Incluye el propio suministro, el transporte, la carga y la descarga del material a pie de obra. Incluye el montaje de todos los elementos del equipo de medida, así como las modificaciones que fuesen necesarias en el resto del sistema, pruebas hasta su correcto funcionamiento, los desplazamientos, pequeño material, herramientas, maquinaria, medios auxiliares. Todo ello con las características técnicas, de montaje, funcionamiento y documentación según especificaciones técnicas de ADIF vigentes.  Con corte de tensión.. Trabajo: Nocturno. ']
textsOK= (texts==refTexts)

# Compute cost.
cost= site.getPrice()
totalRefCost= 26792.40
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
