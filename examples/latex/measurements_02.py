# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

import yaml
import pylatex
from pycost.structure import obra
from pycost.utils import pylatex_utils

# Create main object.
site= obra.Obra(cod="test", tit="Test title")

# Read data from file.
import os
pth= os.path.dirname(__file__)
# print("pth= ", pth)
if(not pth):
    pth= '.'
pendingLinks= site.readFromYaml(pth+'/../../verif/tests/data/yaml/test_file_05.yaml')

doc= pylatex.Document(documentclass= 'book')
doc.packages.append(pylatex.Package('babel', options = ['spanish']))
doc.packages.append(pylatex.Package('minitoc'))
doc.preamble.append(pylatex.Command('selectlanguage', 'spanish'))
# doc.append(pylatex.Command('doparttoc'))
# doc.append(pylatex.Command('parttoc'))
site.writeQuantitiesIntoLatexDocument(doc)

# Generate LaTeX file.
outputFilesBaseName= 'measurements_02'
doc.generate_tex(outputFilesBaseName)

# Remove temporary files.
pylatex_utils.removeLtxTemporaryFiles(outputFilesBaseName)
