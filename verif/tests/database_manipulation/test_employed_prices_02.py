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
from pycost.utils import basic_types

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_file_05.yaml')

employedLabourElementaryPrices= site.getEmployedElementaryPrices(filterByType= basic_types.mdo)
employedLabourElementaryPricesRef= {'PEON', 'PEONES', 'UOFIC0101', 'OFIC', 'OFICMON', 'OFICENC', 'MO0101', 'OFICFER', 'PEONENC', 'OFICJAR', 'MO0201'}

import os
import logging
fname= os.path.basename(__file__)
if (employedLabourElementaryPrices==employedLabourElementaryPricesRef):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
