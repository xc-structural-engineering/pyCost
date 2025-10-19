# -*- coding: utf-8 -*-
'''Trivial PyCost test.''' 
from __future__ import division
from __future__ import print_function

from pycost.structure import obra
from pycost.structure.chapter import Chapter

obra= obra.Obra(cod="test", tit="Test title")

ch01= obra.newSubChapter(Chapter(cod= '01', tit= 'Chapter 01'))
ch02= obra.newSubChapter(Chapter(cod= '02', tit= 'Chapter 02'))
ch02_01= ch02.newSubChapter(Chapter(cod= '02.01', tit= 'Chapter 02.01'))
ch02_02= ch02.newSubChapter(Chapter(cod= '02.02', tit= 'Chapter 02.02'))

totalChapters= len(obra.subcapitulos)+len(ch02.subcapitulos)

import os
import logging
fname= os.path.basename(__file__)
if (totalChapters==4):
    print('test: '+fname+': ok.')
else:
    logging.error('test: '+fname+' ERROR.')
