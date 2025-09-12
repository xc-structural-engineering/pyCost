# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 

import math
import pylatex
from pycost.structure import obra

# Create root chapter.
rootChapter= obra.Obra(cod="test", tit="Test title")

# Create elementary prices.
rootChapter.newElementaryPrice(
    code='MN03020221',
    longDescription='Alquiler de andamio colgado.',
    shortDescription='Alquiler de andamio colgado.',
    price= .03,
    typ=2,
    unit='m3dia'
    )
rootChapter.newElementaryPrice(code= '%CIND', shortDescription= 'Costes indirectos', price= 1, longDescription= 'Costes indirectos', typ= 0, unit= '%')

cPrice= rootChapter.newCompoundPrice(
    code='OCD100',
    shortDescription='Alquiler diario de andamio tubular.',
    longDescription='Alquiler diario de andamio tubular.',
    unit='m3dia',
    components=[
        ('MN03020221', 1.0, 2.0), # ANDAMIO TUBULAR
        ('%CIND', 1.0,0.06),
    ]
)

justificationList= cPrice.components.getPriceJustificationList(True)

total= float(justificationList.getTotal())
roundedTotal= float(justificationList.getRoundedTotal())
totalCP1= float(justificationList.getTotalCP1())

error= (total-0.0636)**2
error+= (roundedTotal-.06)**2
error+= (totalCP1-.06)**2
error= math.sqrt(error)

'''
print('price= ', cPrice.getPrice())
print('justification list length: ', len(justificationList))
print('total: ', total)
print('rounded total: ', roundedTotal)
print('CP1 total: ', totalCP1)
'''

import os
import logging
fname= os.path.basename(__file__)
if (error<1e-12):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')

