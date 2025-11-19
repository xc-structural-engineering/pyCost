# -*- coding: utf-8 -*-
'''Test concept removal.''' 
from __future__ import division
from __future__ import print_function

from pycost.structure import obra

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromJson(pth+'/../data/json/test_file_05.json')

# Compute price before removal.
priceBefore= site.getPrice()

conceptsToRemove= ['PEONES', 'PEONENC'] # Remove this prices and the concepts that depend on it. 
site.removeConcepts(conceptsToRemove)

# Compute price after removal.
priceAfter= site.getPrice()

# Check results.
diff= priceBefore-priceAfter
ratio1= abs(diff-6191.652752400027)/6191.652752400027

'''
print('price before: ', priceBefore)
print('price after: ', priceAfter)
print('difference: ', diff)
print('ratio1= ', ratio1)
'''
import os
import logging
fname= os.path.basename(__file__)
if (ratio1<1e-6):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')


