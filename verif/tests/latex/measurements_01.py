# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

import os
import pylatex
from pycost.utils import pylatex_utils
import logging
import filecmp

# Read data from file.
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
import test_estimates

obra= test_estimates.test(pth)

doc= pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
# doc.append(pylatex.Command('doparttoc'))
# doc.append(pylatex.Command('parttoc'))
obra.writeQuantitiesIntoLatexDocument(doc)

# Generate LaTeX file.
outputFilesBaseName= 'measurements_01'
texFileName= outputFilesBaseName+'.tex'
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

fname= os.path.basename(__file__)
if (ok):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')

# Remove LaTeX file
if os.path.exists(thisFile):
    os.remove(thisFile)
else:
    logging.error('ERROR file: '+thisFile+' not found.')
