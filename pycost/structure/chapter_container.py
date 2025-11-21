# -*- coding: utf-8 -*-
''' Chapter container.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import logging
from decimal import Decimal
import pylatex
from pycost.prices import price_table
from pycost.structure import chapter
from pycost.bc3 import codes
from pycost.bc3 import codigos_obra
from pycost.utils import EntPyCost as epc
from pycost.utils import basic_types
from pycost.measurements import measurement_report

class Subcapitulos(list, epc.EntPyCost):

    def __init__(self,ptr_cap):
        epc.EntPyCost.__init__(self, owner= ptr_cap)

    def getContenedor(self):
        return self

    def setOwner(self, parent):
        ''' Set the parent chapter.

        :param parent: parent chapter.
        '''
        self.owner= parent
        for j in self:
            j.setOwner(parent= parent)
            
    def getHeights(self):
        ''' Return the heights of the chapters.'''
        retval= list()
        for j in self:
            retval.append(j.getHeight())
        return retval
            
    def NumElementales(self, filterBy= None):
        ''' Return the number of elementary prices. If filterBy is not None
        return only the number of elementary prices whose code is also in the
        filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        retval= 0
        for j in self:
            retval+= (j).NumElementales(filterBy= filterBy)
        return retval
    
    def NumDescompuestos(self, filterBy= None):
        ''' Return the number of compound prices. If filterBy is not None
        return only the number of compound prices whose code is also in the
        filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        retval= 0
        for j in self:
            retval+= (j).NumDescompuestos(filterBy= filterBy)
        return retval

    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        for chapter in self:
            chapter.removeConcept(conceptToRemoveCode)
    
    def getConceptsThatDependOn(self, priceCode):
        ''' Return the prices which depend on the one whose code
            is passed as parameter.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        retval= list()
        for chapter in self:
            retval+= chapter.getConceptsThatDependOn(priceCode)
        return retval

    def getPrice(self):
        ''' Compute the cost of the chapters in this container.'''
        retval= 0.0
        for j in self:
            retval+= (j).getPrice()
        return retval

    def getRoundedPrice(self):
        ''' Compute the cost of the chapters in this container using numbers of
            type Decimal.
        '''
        retval= Decimal('0.0')
        for j in self:
            retval+= (j).getRoundedPrice()
        return retval

    def Busca(self, ruta):
        if(len(ruta)==0): return None
        indice= int(ruta[0])-1
        existe= (indice<size())
        if not existe:
            return None
        elif(ruta.size()== 1): #Es subcapitulo de este
            return self[indice]
        else:
            sc= self[indice]
            ruta.pop_front()
            return sc.BuscaSubcapitulo(ruta)
        return None

    def BuscaCodigo(self, nmb):
        retval= None
        for i in self:
            retval= (i).BuscaCodigo(nmb)
            if(retval): return retval

        return retval

    def findPrice(self, cod):
        '''Search a unit price through the chapter tree.'''
        retval= None
        for i in self:
            retval= (i).findPrice(cod)
            if(retval): break
        return retval
    
    def findPricesRegex(self, regex):
        ''' Return the concepts with a code that matches to the regular
            expression argument.

        :param regex: regular expression to match with the concept code.
        '''
        retval= list()
        for chapter in self:
            retval.extend(chapter.findPricesRegex(regex))
        return retval

    def newChapter(self, c):
        ''' Append the given chapter to the container.

        :param c: chapter to append.
        '''
        if(not c.owner):
            c.owner= self.owner
        self.append(c)
        return c

    def newChapterFromRecord(self, r):
        '''Appends a chapter.'''
        nChapter= chapter.Chapter(r.codigo,"",r.factor,r.productionRate)
        nChapter.owner= self.owner
        return self.newChapter(nChapter)

    def newChapters(self, descomp):
        '''Append the chapters from the records on the container.'''
        #sz= len(descomp)
        for comp in descomp:
            self.newChapterFromRecord(comp)

    def LeeBC3Caps(self, co):
        ''' Carga los datos de los subcapítulos de (self).'''
        sc= codes.Codigos(co.GetDatosCaps())
        if len(sc)<1:
            logging.error("No se encontraron subcapitulos." + '\n')

        chapterNames= co.getChapterCodes()

        for i in self:
            code= i.Codigo()
            j= sc.findChapter(code)
            if j:
                reg= sc.getChapterData(code)
                if i:
                    logging.info(u"Loading sub-chapter: '" + reg.Datos().getTitle() + "'\n")
                    i.readBC3(reg) # Title

                    #Lee los elementales del capítulo.
                    elementos_capitulo= co.FiltraElementales(reg.Datos().desc)
                    i.LeeBC3Elementales(elementos_capitulo)
                    if(elementos_capitulo):
                      logging.info("  Loaded " + str(len(elementos_capitulo))
                                   + u" elementary prices of the chapter."
                                   + '\n')
                    co.BorraElementales(elementos_capitulo); #Borra los ya leídos.
                    logging.info("  They remain " + str(len(co.GetDatosElementos())) + " elementary prices." + '\n')

                    #Lee los subcapítulos.
                    i.subcapitulos.newChapters(reg.Datos().filterChapters(chapterNames))
                    i.subcapitulos.LeeBC3Caps(co); #Carga los subcapitulos.


            else:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; chapter with code: '"+ str(i.Codigo())+"' not found.\n")
                continue

    def WriteDescompBC3(self, os, cod):
        if(len(self)<1): return
        os.write("~D" + '|'
           + cod + '|')
        for i in self:
            (i).getBC3Component().WriteBC3(os)
        os.write('|' + '\n')


    def WritePreciosBC3(self, os):
        for i in self:
            (i).WritePreciosBC3(os)

    def WriteBC3(self, os, pos):
        conta= 1
        for i in self:
            nueva_pos= pos+str(conta)+'\\'
            (i).WriteBC3(os,nueva_pos)
            conta+=1

    def ImprCompLtxMed(self, os, parentSection, otro):
        '''Suponemos que ambos capítulos tienen el 
           mismo número de subcapítulos.'''
        sz= len(otro)
        for k in range(0,sz):
            i= self[k]
            j= otro[k]
            i.ImprCompLtxMed(os,parentSection,j)

    def writeQuantitiesIntoLatexDocument(self, doc, sectName, superTabular= False):
        ''' Write quantities in the pylatex document argument.

        :param doc: document to write into.
        :param sectName: section command for the chapter.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''        
        for j in self:
            (j).writeQuantitiesIntoLatexDocument(doc,sectName, superTabular= superTabular)

    def writePriceTableOneIntoLatexDocument(self, doc, sectName, filterBy= None):
        ''' Write unit prices table one in the pylatex document argument.

        :param doc: document to write into.
        :param sectName: section command for the chapter.
        :param filterBy: write the prices on the list only.
        '''
        for j in self:
            (j).writePriceTableOneIntoLatexDocument(doc, sectName, filterBy= filterBy)

    def writePriceTableTwoIntoLatexDocument(self, doc, sectName, filterBy= None):
        ''' Write unit prices table one in the pylatex document argument.

        :param doc: document to write into.
        :param sectName: section command for the chapter.
        :param filterBy: write the prices on the list only.
        '''
        for j in self:
            (j).writePriceTableTwoIntoLatexDocument(doc, sectName, filterBy= filterBy)

    def writeElementaryPrices(self, doc, parentSection, tipos=  [basic_types.mdo, basic_types.maq, basic_types.mat], filterBy= None, superTabular= False):
        ''' Write the elementary prices table.

        :param doc: pylatex document to write into.
        :param parentSection: section command for the parent chapter.
        :param tipos: types of the prices to write (maquinaria, materiales o mano de obra) defaults to all of them.
        :param filterBy: write those prices only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        for j in self:
            (j).writeElementaryPrices(doc, parentSection, tipos, filterBy= filterBy, superTabular= superTabular)

    def writePriceJustification(self, data_table, parentSection, filterBy= None):
        ''' Write unit prices table one in the pylatex document argument.

        :param data_table: pylatex tabular data to populate.
        :param parentSection: section command for the parent chapter.
        :param filterBy: write price justification for those prices only.
        :returns: list of the written prices.
        '''
        retval= list()
        for j in self:
            retval+= (j).writePriceJustification(data_table, parentSection= parentSection, filterBy= filterBy)
        return retval

    def ImprLtxResumen(self, doc, parentSection, recursive):
        ''' Write summary report.

        :param doc: pylatex document to write into.
        :param parentSection: section command for the parent chapter.
        :param recursive: if true apply recursion through chapters.
        '''
        if len(self):
            with doc.create(pylatex.Itemize()) as itemize:
                for j in self:
                    (j).ImprLtxResumen(itemize,parentSection,recursive)

    def ImprCompLtxPre(self, doc, parentSection, other):
        '''Compare chapters.

        :param doc: pylatex document to write into.
        :param parentSection: section command for the parent chapter.
        :param other: chapter to compare with.
        '''
        for i, j in zip(self, other):
            i.ImprCompLtxPre(doc,parentSection,j)

    def writePartialBudgetsIntoLatexDocument(self, doc, sectName, superTabular= False):
        ''' Write partial budgets into the pylatex document argument.

        :param doc: pylatex document to write into.
        :param sectName: section command for the chapter.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        for j in self:
            (j).writePartialBudgetsIntoLatexDocument(doc,sectName, superTabular= superTabular)

    def writeSpreadsheetSummary(self, sheet, depth, recursive, maxDepth):
        ''' Write summary report.

        :param sheet: spreadsheet to write into.
        :param parentSection: section command for the parent chapter.
        :param recursive: if true apply recursion through chapters.
        '''
        if len(self):
            for j in self:
                (j).writeSpreadsheetSummary(sheet= sheet, depth= depth, recursive= recursive, maxDepth= maxDepth)

    def writeSpreadsheetQuantities(self, sheet, parentSection):
        ''' Write the quantities in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        :param parentSection: name of the parent section.
        '''
        for j in self:
            (j).writeSpreadsheetQuantities(sheet, parentSection)

    def writeSpreadsheetBudget(self, sheet, parentSection):
        ''' Write the partial budgets in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        :param parentSection: name of the parent section.
        '''
        for j in self:
            (j).writeSpreadsheetBudget(sheet, parentSection)

    def hasQuantities(self):
        '''Returns true if al least one of the chapters have quantities.'''
        retval= False
        for c in self:
            if c.hasQuantities():
                retval= True
                break
        return retval
    
    def getQuantitiesReport(self):
        retval= measurement_report.QuantitiesReport()
        for j in self:
            retval.Merge((j).getQuantitiesReport())
        return retval

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= epc.EntPyCost.getDict(self)
        components= dict()
        for chapter in self:
            code= chapter.Codigo()
            components[code]= chapter.getDict()
        retval['components']= components
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= list() # Links that cannot be set yet.
        components= dct['components']
        if(components):
            for key in components:
                chapterDict= components[key]
                ch= chapter.Chapter(key)
                pendingLinks.extend(ch.setFromDict(chapterDict))
                self.append(ch)
            pendingLinks.extend(epc.EntPyCost.setFromDict(self, dct))
        return pendingLinks

    def clear(self):
        '''removes all items from the chapter.'''
        for sc in self:
            sc.clear()
        super(Subcapitulos,self).clear()
