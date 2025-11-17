# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

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


# Check ownership.
testOK= True
for chapter_code in ['CAP1.1#', 'CAPITULO2#', 'CAPITULO3#', 'CAP.1.7.1#', 'CAP1.6.1#']:
    chapter= site.findChapter(chapterCode= chapter_code)
    rootChapter= chapter.getRootChapter()
    if(rootChapter.Codigo()!=site.Codigo()):
        testOK= False

import os
import logging
fname= os.path.basename(__file__)
if testOK:
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')

