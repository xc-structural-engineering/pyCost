# -*- coding: utf-8 -*-
'''Trivial PyCost test. Check getRootChapter method.''' 
from __future__ import division
from __future__ import print_function

from pycost.structure import obra
from pycost.structure.chapter import Chapter

root= obra.Obra(cod="test", tit="Test title")

ch01= root.newSubChapter(Chapter(cod= '01', tit= 'Chapter 01'))

rootChapter= ch01.getRootChapter()

idRootChapter= id(rootChapter)
idRoot= id(root)

'''
print(idRootChapter)
print(idRoot)
'''

import os
import logging
fname= os.path.basename(__file__)
if (idRootChapter==idRoot):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
