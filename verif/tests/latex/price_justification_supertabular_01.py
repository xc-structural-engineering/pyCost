# -*- coding: utf-8 -*-
'''Test price justification writing.'''

from __future__ import division
from __future__ import print_function

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2025, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es" "ana.Ortega@ciccp.es"

import os
import pylatex
from pycost.utils import pylatex_utils
from pycost.structure import obra
import logging
import filecmp

rootChapter= obra.Obra(cod="test", tit="Test title")

# Read data from file.
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
rootChapter.readFromYaml(pth+'/../data/yaml/test_03_prices.yaml')

# Store text int pylatex doc.
doc= pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('supertabular'))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
# doc.append(pylatex.Command('doparttoc'))
# doc.append(pylatex.Command('parttoc'))
rootChapter.writePriceJustification(doc, signaturesFileName= None, superTabular= True)


# Generate LaTeX file.
fname= os.path.basename(__file__)
outputFilesBaseName= fname[:-3]
texFileName= fname.replace('.py', '.tex')
thisFile= pth+'/./'+outputFilesBaseName
doc.generate_tex(thisFile)
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
if(ok):
    if os.path.exists(thisFile):
        os.remove(thisFile)
    else:
        logging.error('ERROR file: '+thisFile+' not found.')
