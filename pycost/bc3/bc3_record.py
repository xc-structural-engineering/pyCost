# -*- coding: utf-8 -*-
''' BC3 record.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pycost.bc3 import fiebdc3
import logging

elemento, descompuesto, medicion, obra, capitulo, sin_tipo= range(0,6)

class RegBC3(object):
    def __init__(self, code):
        self.code= code # Concept identifier.
        self.c= None # Concepto
        self.d= None # Descomposición.
        self.m= None # Medicion
        self.t= None # Texto
        self.y= None # Descomposición.
        self.p= None # Parameter definitions.

    def GetDatosElemento(self):
        return fiebdc3.regBC3_elemento(self.GetConcepto(),self.GetTexto())

    def getUnitPriceData(self):
        '''Return the data corresponding to a unit cost concept.'''
        return fiebdc3.regBC3_udobra(self.GetConcepto(),self.GetTexto(),self.GetDesc())

    def GetDatosMedicion(self):
        return fiebdc3.regBC3_medicion(self.GetConcepto(),self.GetTexto(),self.GetMed())

    def GetConcepto(self):
        return fiebdc3.regBC3_c(self.c)

    def GetTexto(self):
        return fiebdc3.regBC3_t(self.t)

    def getParametricData(self):
        return fiebdc3.regBC3_parametric(self.GetConcepto(), self.GetTexto(), self.getParameters())

    def getParameters(self):
        ''' Return the parametric concept contained in the BC3 file.'''
        return fiebdc3.regBC3_p(self.p)

    def GetDesc(self):
        tmp= None
        if(self.d and self.y):
            tmp= self.d+self.y
        elif(self.d):
            tmp= self.d
        elif(self.y):
            tmp= self.y
        bc3String= ''
        if(tmp): # if it's composed.
            for s in tmp:
                bc3String+= s
        return fiebdc3.regBC3_d(bc3String)


    def GetMed(self):
        return fiebdc3.regBC3_m(self.m)

    def isParametric(self):
        ''' Return true if the concept is a parametric one.'''
        return (self.p is not None)

    def isElementaryCost(self):
        '''Return true if the entity corresponds to an elementary cost.'''
        return ((self.d is None) and (self.y is None) and (self.m is None) and (self.p is None))

    def EsDescompuesto(self):
        '''Return true if the entity corresponds to a unit cost.'''
        if(self.EsMedicion()):
            return False
        elif(self.isElementaryCost()):
            return False
        elif(self.isChapterOrObra()):
            return False
        else:
            return True
        
    def EsMedicion(self):
        '''Return true if the entity corresponds to a measurement.'''
        return not (self.m is None)


    def getConceptType(self):
        ''' Return the type of this concept.'''
        if self.EsObra():
            return obra
        elif self.isElementaryCost():
            return elemento
        elif self.EsMedicion():
            return medicion
        elif self.EsDescompuesto():
            return descompuesto
        elif self.isChapter():
            return capitulo
        else:
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            logging.error(className+'.'+methodName+"; type of the concept: '" + str(i) + "' not found.")
            return sin_tipo

    def getConceptTypeString(self):
        ''' Return a string identifying the type of this concept.'''
        retval= "sin_tipo"
        tipo= self.getConceptType()
        if(tipo==obra):
            retval= "obra"
        elif(tipo==elemento):
            retval= "elemento"
        elif(tipo==medicion):
            retval= "medicion"
        elif(tipo==descompuesto):
            retval= "descompuesto"
        elif(tipo==capitulo):
            retval= "capitulo"
        return retval

    def EsObra(self):
        ''' Return true if this concept corresponds to the root chapter.'''
        return fiebdc3.es_codigo_obra(self.code)
    
    #not  @brief Devuelve verdadero si el concepto corresponde a un capitulo.
    def isChapter(self):
        if self.isChapterOrObra():
            return not self.EsObra()
        else:
            return False
        #return fiebdc3.es_codigo_capitulo(self.c)

    def isChapterOrObra(self):
        if(self.EsMedicion()): #Quantities have the code of their chapter.
            return False
        else:
            return fiebdc3.es_codigo_capitulo_u_obra(self.code)

    def getChapterData(self):
        return fiebdc3.regBC3_capitulo(self.GetConcepto(), self.GetTexto(), self.GetDesc())


    def Print(self,os):
        os.write("C: " + self.c + ' ' + self.c.size() + '\n'
           + "D: " + self.d + ' ' + self.d.size() + '\n'
           + "M: " + self.m + ' ' + self.m.size() + '\n'
           + "T: " + self.t + ' ' + self.t.size() + '\n'
           + "Y: " + self.y + ' ' + self.y.size() + '\n'
           + "P: " + self.p + ' ' + self.p.size() + '\n')
        return os

