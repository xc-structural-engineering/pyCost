# -*- coding: utf-8 -*-
'''Test generation of budget summary.'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2025, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import os
import pylatex
from pycost.utils import basic_types
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

# Store text in pylatex doc.
## Materials.
materials_doc=pylatex.Document(documentclass= 'book')
employedElementaryPrices= rootChapter.getEmployedElementaryPrices()
rootChapter.writeElementaryPrices(materials_doc, tipos= [basic_types.mat],filterBy= employedElementaryPrices, superTabular= True, sctName= None)
materialListFName= 'materials_list.tex'
materialsOutputFName= pth+'/./'+materialListFName
## Machinery.
machinery_doc=pylatex.Document(documentclass= 'book')
employedElementaryPrices= rootChapter.getEmployedElementaryPrices()
rootChapter.writeElementaryPrices(machinery_doc, tipos= [basic_types.maq],filterBy= employedElementaryPrices, superTabular= True, sctName= None)
machineryListFName= 'machinery_list.tex'
machineryOutputFName= pth+'/./'+machineryListFName
## Labour.
labour_doc=pylatex.Document(documentclass= 'book')
employedElementaryPrices= rootChapter.getEmployedElementaryPrices()
rootChapter.writeElementaryPrices(labour_doc, tipos= [basic_types.mdo],filterBy= employedElementaryPrices, superTabular= True, sctName= None)
labourListFName= 'labour_list.tex'
labourOutputFName= pth+'/./'+labourListFName

# Generate LaTeX file.
fname= os.path.basename(__file__)
outputFilesBaseName= fname[:-3]
## Materials.
materialsFile= pth+'/./mat_'+outputFilesBaseName
materials_doc.generate_tex(materialsFile)
materialsFile+= '.tex'
## Machinery.
machineryFile= pth+'/./maq_'+outputFilesBaseName
machinery_doc.generate_tex(machineryFile)
machineryFile+= '.tex'
## Labour.
labourFile= pth+'/./mdo_'+outputFilesBaseName
labour_doc.generate_tex(labourFile)
labourFile+= '.tex'

# Extract contents.
## Materials.
pylatex_utils.extract_latex_document_contents(inputFile= materialsFile, outputFile= materialsOutputFName)
## Machinery.
pylatex_utils.extract_latex_document_contents(inputFile= machineryFile, outputFile= machineryOutputFName)
## Labour.
pylatex_utils.extract_latex_document_contents(inputFile= labourFile, outputFile= labourOutputFName)

# Compare with reference file.
materialsRefFile= pth+'/../data/latex/ref_'+materialListFName
machineryRefFile= pth+'/../data/latex/ref_'+machineryListFName
labourRefFile= pth+'/../data/latex/ref_'+labourListFName

materialsOK= filecmp.cmp(materialsRefFile, materialsOutputFName, shallow=False)
machineryOK= filecmp.cmp(machineryRefFile, machineryOutputFName, shallow=False)
labourOK= filecmp.cmp(labourRefFile, labourOutputFName, shallow=False)

# print(ok)
# print(thisFile)

testOK= (materialsOK and machineryOK and labourOK)
if testOK:
    print('test: '+fname+': ok.')
else:
    logging.error('materials OK: '+ str(materialsOK))
    logging.error('machinery OK: '+ str(machineryOK))
    logging.error('labour OK: '+ str(labourOK))
    logging.error('test: '+fname+' ERROR.')

# Remove LaTeX files
if testOK:
    for fName in [materialsFile, materialsOutputFName, machineryFile, machineryOutputFName, labourFile, labourOutputFName]: 
        if os.path.exists(fName):
            os.remove(fName)
        else:
            logging.error('ERROR file: '+fName+' not found.')
