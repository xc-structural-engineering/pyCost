# -*- coding: utf-8 -*-
''' Concept dictionary.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import logging
from pycost.utils import EntPyCost as epy

class KeyMap(dict):
    def __init__(self):
        super(KeyMap,self).__init__()


class ConceptDict(epy.EntPyCost):
    #claves= KeyMap() claves key map has been DEPRECATED.
    def __init__(self):
        ''' Constructor.'''
        super(ConceptDict,self).__init__()
        self.concepts= dict()
        
    def __len__(self):
        return len(self.concepts)
    
    def Append(self, u):
        ''' Append the argument to the concept dictionary.'''
        key= u.Codigo()
        #self.claves[key]= u
        self.concepts[key]= u
        return u

    @staticmethod
    def err_no_encontrado(cod):
        className= type(self).__name__
        methodName= sys._getframe(0).f_code.co_name
        logging.error(className+'.'+methodName+"; concept: " + cod + " not found.")

    def Busca(self,cod):
        retval= None
        # if cod in self.claves:
        #     retval= self.claves[cod]
        if cod in self.concepts:
            retval= self.concepts[cod]
        return retval

    def findRegex(self, regex):
        ''' Return the concepts with a code that matches to the regular
            expression argument.

        :param regex: regular expression to match with the concept code.
        '''
        retval= list()
        # for key in self.claves:
        #     if(not regex.match(key) is None):
        #         retval.append(self.claves[key])
        for key in self.concepts:
            if(not regex.match(key) is None):
                retval.append(self.concepts[key])
        return retval
        
        

    def WriteBC3(self,os):
        for j in self.concepts.keys():
           self.concepts[j].WriteBC3(os)

    def Write(self,os):
        for j in self.concepts.keys():
           self.concepts[j].Write(os)

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(ConceptDict, self).getDict()
        for key in self.concepts:
            value= self.concepts[key]
            retval[key]= value.getDict()
        return retval

    def clear(self):
        '''removes all items from the container.'''
        self.concepts.clear()
        

def find_concept(conceptName):
    logging.error('find_concept has been deprecated. Use the getUnitPrice method of the root chapter.')
    return None
