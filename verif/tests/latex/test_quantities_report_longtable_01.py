# -*- coding: utf-8 -*-
'''Extract concepts from unit cost databases.''' 
from __future__ import division
from __future__ import print_function

import sys
import yaml
from pycost.structure import obra
from pycost.utils import pylatex_utils
import filecmp
import logging

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromYaml(pth+'/../data/yaml/test_file_05.yaml')

report= site.getPriceReportLatexDocument(superTabular= False)

# Generate LaTeX file.
fname= os.path.basename(__file__)
outputFilesBaseName= fname[:-3]
texFileName= fname.replace('.py', '.tex')
thisFile= pth+'/./'+outputFilesBaseName
report.generate_tex(thisFile)
thisFile+= '.tex'

# Remove temporary files (if any).
pylatex_utils.removeLtxTemporaryFiles(outputFilesBaseName)

# Compare with reference file.
refFile= pth+'/../data/latex/ref_'+texFileName

ok= filecmp.cmp(refFile, thisFile, shallow=False)

# print(ok)
# print(thisFile)

if (ok):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')

# Remove LaTeX file
if os.path.exists(thisFile):
    os.remove(thisFile)
else:
    logging.error('ERROR file: '+thisFile+' not found.')
