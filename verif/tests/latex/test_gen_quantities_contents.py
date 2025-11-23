# -*- coding: utf-8 -*-
'''Test generation of budget summary.'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2025, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

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
rootChapter.readFromJson(pth+'/../data/json/test_file_09.json')

doc=pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.packages.append(pylatex.Package('supertabular'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
doc.append(pylatex.Command('doparttoc'))
rootChapter.writeQuantitiesIntoLatexDocument(doc, superTabular= True)

# Generate LaTeX file.
fname= os.path.basename(__file__)
outputFilesBaseName= fname[:-3]
texFileName= fname.replace('.py', '.tex')
thisFile= pth+'/./'+outputFilesBaseName
doc.generate_tex(thisFile)
thisFile+= '.tex'

# Extract contents.
pylatex_utils.extract_latex_document_contents(inputFile= thisFile, outputFile= thisFile)

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
