# -*- coding: utf-8 -*-
'''Test price justification writing.'''

from __future__ import division
from __future__ import print_function

import os
import pylatex
from pycost.utils import pylatex_utils
from pycost.structure import obra
from pycost.utils import basic_types
import logging
import filecmp

rootChapter= obra.Obra(cod="test", tit="Test title")

# Read data from file.
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
rootChapter.readFromYaml(pth+'/../data/yaml/test_file_05.yaml')

filterBy= ['MQRETR0102', 'PEON', 'MQCAMI0101', '%003', 'UTAMIZ', 'UPALA0101', 'UTRITU', 'UCOMP0202', 'UCAMI0201', 'UMOTO0102', 'OFICFER', 'PEONES', 'MAACE0201', 'OFICMON', 'TH66072', 'TK26300', 'Q004', 'Q003', '%UMAUX0103', 'OFICJAR', 'MMME.6a', 'MO0101', 'MO0201', 'UHORACERO', 'C2003000', 'PULI', 'UZAHO0102', 'UBULL0101', 'UAREN0103']

# Store text int pylatex doc.
doc= pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
# doc.append(pylatex.Command('doparttoc'))
# doc.append(pylatex.Command('parttoc'))
rootChapter.writeElementaryPrices(doc, tipos= [basic_types.mdo, basic_types.maq, basic_types.mat], filterBy= filterBy)


# Generate LaTeX file.
outputFilesBaseName= 'employed_elementary_prices'
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
