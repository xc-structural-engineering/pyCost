# -*- coding: utf-8 -*-
'''Parametric concepts as defined in the FIEBDC-3 specification.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2022, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"


import logging
from pycost.bc3 import fiebdc3
from pycost.prices import unit_price
from pycost.bc3 import fr_entity
from pycost.bc3 import bc3_component

class Parametric(fiebdc3.regBC3_parametric):
    ''' Parametric concept as defined in the FIEBDC-3 specification.'''
    
    def __init__(self,c= None,t= None,p= None):
        ''' Constructor.

        :param c: concept.
        :param t: text.
        :param p: parameters.
        '''
        super(Parametric, self).__init__(c,t,p)

    def getUnitPrice(self, code, options, rootChapter):
        ''' Return a unit cost instantiating this object.

        :param code: code for the new unit cost.
        :param options: list of (parameterKey, parameterOption) tuples assigning
                        values to the parameters.
        :param rootChapter: root chapter (access to the already 
                            defined concepts).
        '''
        codeTail= self.getCodeTail(options)
        code= code.replace('$', codeTail)
        components= self.getComponents(options)
        summary= self.getSummary(options)
        text= self.getText(options)
        retval= unit_price.UnitPrice(cod= code, desc= summary, ud= self.Unidad(), ld= text)
        # Populate component list.
        cList= retval.components
        for key in components:
            searchKey= key
            if('%' in key):
                searchKey= key[1:] # Remove the first percent sign.
            ent= rootChapter.getUnitPrice(searchKey)
            if not ent:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.warning(className+'.'+methodName+"; component: " + key + ' not found.')
                error= True
                continue
            else:
                value= components[key]
                fr= fr_entity.EntFR(f= 1.0, r= value)
                cList.append(bc3_component.BC3Component(ent,fr))
                error= False
        
        return retval
    
