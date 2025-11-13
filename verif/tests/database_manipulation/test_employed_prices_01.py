# -*- coding: utf-8 -*-
'''Extract concepts from unit cost databases.''' 
from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import yaml
from pycost.structure import obra

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_file_05.yaml')

employedPrices= site.getEmployedPrices(lowerMeasurementBound= 1000.0)
employedPricesRef= {'DSELECRI', 'DRIESUB', 'USJT10abz', 'RELL0301', 'DPAVHORPUL', 'ACERO0103', 'DALPEDR', 'DMOVI3001'}

employedElementaryPrices= site.getEmployedElementaryPrices(lowerMeasurementBound= 1000.0)
employedElementaryPricesRef= {'PEONES', 'UPALA0101', 'MO0201', 'UCAMI0201', 'TK26300', 'MQRETR0102', '%UMAUX0103', 'UCOMP0202', 'MO0101', 'UBULL0101', 'UZAHO0102', 'PULI', 'TH66072', 'UAREN0103', 'OFICMON', 'Q003', 'UMOTO0102', 'MAACE0201', 'MMME.6a', 'Q004', '%003', 'UTRITU', 'UHORACERO', 'OFICFER', 'PEON', 'UTAMIZ', 'MQCAMI0101', 'C2003000', 'OFICJAR'}

'''
print(employedPrices)
print(employedElementaryPrices)
'''

import os
import logging
fname= os.path.basename(__file__)
if (employedPrices==employedPricesRef) and (employedElementaryPrices==employedElementaryPricesRef):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
