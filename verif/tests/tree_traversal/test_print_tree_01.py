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
import filecmp
from pycost.structure import obra
from pycost.measurements import measurement_report
from pycost.utils import basic_types

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
fname= os.path.basename(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_file_05.yaml')

outputFileName= fname.replace('.py', '.txt')
refFileName= pth+'/../data/reference_files/ref_'+outputFileName

# Write tree.
with open(outputFileName, 'w') as f:
    site.printTree(os= f, includeTitles= False)

# Check results.
testOK= filecmp.cmp(outputFileName, refFileName, shallow=False)

# site.printTree()

import logging
if testOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')

# Clean after yourself.
if os.path.exists(outputFileName):
    os.remove(outputFileName)

