# -*- coding: utf-8 -*-
''' Chapter.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import logging
import sys
import pylatex
import re
import json
from decimal import Decimal
from pycost.measurements import measurement_container
from pycost.bc3 import fr_entity
from pycost.bc3 import bc3_entity
from pycost.bc3 import bc3_component
from pycost.structure import chapter_container
from pycost.prices import price_table
from pycost.prices import unit_price_container
from pycost.structure import unit_price_quantities
from pycost.utils import pylatex_utils
from pycost.utils import basic_types

class Chapter(bc3_entity.EntBC3):
    ''' Chapter.

    :ivar fr: factor and production rate values.
    :ivar subcapitulos: sub-chapters.
    :ivar quantities: chapter quantities.
    :ivar precios: chapter price table.
    '''
    precision= 2
    places= Decimal(10) ** -precision
    formatString= '{0:.'+str(precision)+'f}'
    
    def __init__(self, cod= "CapSinCod", tit= "CapSinTit", factor= 1.0, productionRate= 1.0):
        ''' Constructor.

        :param cod: chaper codename.
        :param tit: chapter title.
        :param factor:
        :param productionRate: production rate.
        '''
        super(Chapter,self).__init__(cod,tit)
        self.fr= fr_entity.EntFR(factor,productionRate)
        self.subcapitulos= chapter_container.Subcapitulos(self)
        self.quantities= measurement_container.ChapterQuantities()
        self.precios= price_table.CuaPre() #Para precios elementales y
                               #descompuestos clasificados por capítulos.

    def isRootChapter(self):
        ''' Returns false.'''
        return False
    
    def newElementaryPrice(self, code, shortDescription, price, typ, unit, longDescription= None):
        ''' Define an elementary price.

        :param code: price identifier.
        :param shortDescription: short description of the price.
        :param typ: price type (labor, machinery, materials or unclassified).
        :param unit: unit (m, kg,...).
        :param longDescription: long description of the price.
        '''
        return self.precios.newElementaryPrice(code= code, shortDescription= shortDescription, price= price, typ= typ, unit= unit, longDescription= longDescription)

    def NumElementales(self, filterBy= None):
        ''' Return the number of elementary prices in this chapter and its
            sub-chapters. If filterBy is not None return only the number of 
            elementary prices whose code is also in the filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        return self.precios.NumElementales(filterBy= filterBy)+self.subcapitulos.NumElementales(filterBy= filterBy)
    
    def TieneElementales(self, filterBy= None):
        ''' Return true if the chapter has elementary prices. If filterBy 
        is not None return true only if the number of elementary prices 
        whose code is also in the filterBy list is not zero.

        :param filterBy: count only the codes on this list.
        '''
        return (self.NumElementales(filterBy= filterBy)>0)
    
    def NumDescompuestos(self, filterBy= None):
        ''' Return the number of compound prices in this chapter and its
            sub-chapters. If filterBy is not None return only the number of 
            compound prices whose code is also in the filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        return self.precios.NumDescompuestos(filterBy= filterBy)+self.subcapitulos.NumDescompuestos(filterBy= filterBy)
    
    def newCompoundPrice(self, code, shortDescription, components, unit, longDescription= None):
        ''' Define a compound price.

        :param code: price identifier.
        :param shortDescription: short description of the price.
        :param components: price decomposition.
        :param unit: unit (m, kg,...).
        :param longDescription: long description of the price.
        '''
        # Dereference the prices in the component list.
        derefComponents= list()
        for comp in components:
            key= comp[0]
            price= self.findPrice(key)
            if(price):
                tpl= (price, comp[1], comp[2])
                derefComponents.append(tpl)
            else:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; Price: "+str(key)+' not found.')
        retval= self.precios.newCompoundPrice(code= code, shortDescription= shortDescription, components= derefComponents, unit= unit, longDescription= longDescription)
        return retval
        
    def TieneDescompuestos(self, filterBy= None):
        ''' Return true if the chapter has compound prices. If filterBy 
        is not None return true only if the number of compound prices 
        whose code is also in the filterBy list is not zero.

        :param filterBy: count only the codes on this list.
        '''
        return (self.NumDescompuestos(filterBy= filterBy)>0)
    
    def getConceptsThatDependOn(self, priceCode):
        ''' Return the prices or quantities which depend on the one whose code
            is passed as parameter.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        retval= self.precios.getConceptsThatDependOn(priceCode)
        retval+= self.subcapitulos.getConceptsThatDependOn(priceCode)
        retval+= self.quantities.getConceptsThatDependOn(priceCode)
        return retval

    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        self.quantities.removeConcept(conceptToRemoveCode)
        self.subcapitulos.removeConcept(conceptToRemoveCode)
        self.precios.removeConcept(conceptToRemoveCode)
        
    def removeConcepts(self, codesToRemove):
        ''' Remove the concepts whose codes are being passed as parameter.

        :param codesToRemove: list with the codes of the concepts to remove.
        '''
        for code in codesToRemove:
            self.removeConcept(code)
    
    def replacePrices(self, replacementsTable):
        ''' Replace the prices as indicated by the pairs 
            [oldPriceCode, newPrice] in the argument table.

        :param replacementsTable: list of replacement pairs.
        '''
        affectedConcepts= list()
        for pair in replacementsTable:
            # Retrieve the affected records.
            oldPriceCode= pair[0]
            affectedConcepts+= self.getConceptsThatDependOn(oldPriceCode)
            # Then replace the old price by the new one.
            newPrice= pair[1]
            for concept in affectedConcepts:
                concept.replaceConcept(oldPriceCode, newPrice)
            # And get rid of the old concept.
            self.removeConcept(oldPriceCode)
            
    def GetBuscadorDescompuestos(self):
        return self.precios.GetBuscadorDescompuestos()
    
    def getSubcapitulos(self):
        return self.subcapitulos
    
    def getQuantities(self):
        return self.quantities
    
    def hasQuantities(self):
        retval= False
        if(self.quantities):
            retval= True
        else:
            for s in self.subcapitulos:
                if(s.hasQuantities()):
                    retval= True
                    break
        return retval
    
    def getLtxPriceString(self):
        ''' Return the price in as a string in human readable format.'''
        return basic_types.human_readable_currency(self.getRoundedPrice())
    
    def WriteQuantitiesBC3(self,os, pos=""):
        self.quantities.Write(os,self.CodigoBC3(),pos)
    def WriteSubChaptersBC3(self,os, pos=""):
        self.subcapitulos.WriteBC3(os,pos)
    def CodigoBC3(self):
        return super(Chapter,self).CodigoBC3() + "#"
    def CuadroPrecios(self):
        return self.precios
    def appendUnitPriceQuantities(self, m):
        ''' Append the UnitPriceQuantities object to the quantities container.

        :param m: quantities to append.
        '''
        self.quantities.append(m)
    def appendQuantitiesList(self, priceCode, measurements):
        ''' Append the given list of quantities to the quantities container.

        :param priceCode: code of the price of the material being quantified.
        :param measurements: list of (remark, numberOfUnits, lenght, width, height) tuples.
        '''
        root= self.getRootChapter()
        quantities= unit_price_quantities.UnitPriceQuantities(root.getUnitPrice(priceCode))
        for row in measurements:

            quantities.appendMeasurement(textComment=row[0], nUnits= row[1], length= row[2], width= row[3], height= row[4])
        self.appendUnitPriceQuantities(quantities)
        
        
    def getBC3Component(self):
        '''Return this chapter as a component.'''
        return bc3_component.BC3Component(e= self,fr= self.fr)
    def LeeBC3Elementales(self, elementos):
        '''Appends the elementary prices from argument.'''
        self.precios.LeeBC3Elementales(elementos)
    def LeeBC3DescompFase1(self, descompuestos):
        self.precios.LeeBC3DescompFase1(descompuestos)
    def LeeBC3DescompFase2(self, descompuestos, rootChapter):
        return self.precios.LeeBC3DescompFase2(descompuestos, rootChapter= rootChapter)
    
    def BuscaSubcapitulo(self, ruta):
        retval= None
        if ruta:
            retval= self.subcapitulos.Busca(ruta)
            if not retval:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; chapter with code: " + ruta[1] + " not found in chapter: '"+str(self.Codigo()) + " (" + self.getTitle()
                          + ") (ruta: " + ruta + ')' + '\n')
                #Si no encuentra el capítulo devuelve este mismo
                retval= self
        return retval
    
    def BuscaSubcapitulo(self, lst):
        '''Search the sub-chapter indicated by
           the given list, which has the form ['1', '2', '1', '4']. '''
        retval= None
        sz= len(lst)
        if(sz>0): # not empty.
            indice= int(lst.pop(0))
            if(indice>len(self.subcapitulos)):
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; chapter with index: " + str(indice) + " not found in chapter: '"+str(self.Codigo()) + "' returning None.\n")
                return None
            if(sz==1): # it must be a subchapter of this one.
                retval= self.subcapitulos[indice-1]
                return retval
            elif(sz>1): # still diging.
                return self.subcapitulos[indice-1].BuscaSubcapitulo(lst)
        else:
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            logging.error(className+'.'+methodName+"; empty list argument: " + str(lst) + " in chapter: '"+str(self.Codigo()) + "' returning None.\n")
            return None

        logging.error("sale por aqui (y no debiera) en el capitulo: " + self.Codigo() + '\n')
        return retval
    
    def BuscaCodigo(self, nmb):
        if (self.Codigo()==nmb) or ((self.Codigo()+'#')==nmb):
            return self
        else:
            return self.subcapitulos.BuscaCodigo(nmb)
        
    def BuscaCodigo(self, nmb):
        if self.Codigo()==nmb:
            return self
        else:
            return self.subcapitulos.BuscaCodigo(nmb)
        
    def findPrice(self, cod):
        ''' Return the concept with the code corresponding to the argument.

        :param cod: code of the concept to find.
        '''
        retval= self.precios.findPrice(cod)
        if not retval:
            retval= self.subcapitulos.findPrice(cod)
        return retval

    def findPricesRegex(self, regex):
        ''' Return the concepts with a code that matches to the regular
            expression argument.

        :param regex: regular expression to match with the concept code.
        '''
        retval= self.precios.findPricesRegex(regex)
        retval.extend(self.subcapitulos.findPricesRegex(regex))
        return retval
    
    def extractConcepts(self, conceptCodes, recipientChapter):
        ''' Dumps the concepts corresponding to the codes in the argument list
            in the recipient chapter.

        :param conceptCodes: concepts to extract.
        :param recipientChapter: chapter that will receive the 
                                 extracted concepts.
        '''
        for cCode in conceptCodes:
            # Search concept.
            price= self.findPrice(cCode)
            if(price):
                price.appendToChapter(recipientChapter)
        return recipientChapter
    
    def extractConceptsRegex(self, conceptCodes, recipientChapter):
        ''' Dumps the concepts corresponding to the codes in the argument list
            in the recipient chapter.

        :param conceptCodes: concepts to extract.
        :param recipientChapter: chapter that will receive the 
                                 extracted concepts.
        '''
        for cCode in conceptCodes:
            # Search for elementary price.
            testExpr= re.compile(cCode)
            prices= self.findPricesRegex(testExpr)
            if(len(prices)>0):
                for p in prices:
                    p.appendToChapter(recipientChapter)
        return recipientChapter

    def newSubChapter(self, c):
        ''' Append the given chapter to the container.

        :param c: chapter to append.
        '''
        c.owner= self
        return self.subcapitulos.newChapter(c)

    def extractChapters(self, chapterCodes, recipientChapter):
        ''' Dumps the concepts corresponding to the codes in the argument list
            in the recipient chapter.

        :param conceptCodes: concepts to extract.
        :param recipientChapter: chapter that will receive the 
                                 extracted concepts.
        '''
        employedPrices= set()
        for chapterCode in chapterCodes:
            # Search concept.
            chapter= self.BuscaCodigo(chapterCode)
            if(chapter):
                employedPrices.update(chapter.getEmployedPrices())
                recipientChapter.subcapitulos.newChapter(chapter)
        recipientChapter= self.extractConcepts(employedPrices, recipientChapter)
        return recipientChapter
    
    def WritePreciosBC3(self, os):
        self.precios.WriteBC3(os)
        self.subcapitulos.WritePreciosBC3(os)
        
    def WriteDescompBC3(self, os):
        self.subcapitulos.WriteDescompBC3(os,self.CodigoBC3())
        self.quantities.WriteDescompBC3(os,self.CodigoBC3())
        
    def WriteBC3(self, os, pos):
        self.WriteConceptoBC3(os)
        self.WriteDescompBC3(os)
        self.WriteQuantitiesBC3(os,pos)
        self.WriteSubChaptersBC3(os,pos)

    def getMembersDict(self):
        ''' Return a dictionary containing the data of the chapter members.'''
        retval= dict()
        retval['sub_chapters']= self.subcapitulos.getDict()
        retval['prices']= self.precios.getDict()
        retval['chapter_quantities']= self.quantities.getDict()
        return retval

    def setMembersFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= self.quantities.setFromDict(dct['chapter_quantities'])
        pendingLinks.extend(self.precios.setFromDict(dct['prices']))
        pendingLinks.extend(self.subcapitulos.setFromDict(dct['sub_chapters']))
        return pendingLinks
    
    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(Chapter, self).getDict()
        retval.update(self.getMembersDict())
        return retval
        
    def setFromDict(self,dct):
        ''' Read object from a dictionary.

        :param dct: input dictionary.
        '''
        if(isinstance(dct, list)): # deal with xmltodict imported dictionaries.
            dct= dct[0]
        pendingLinks= self.setMembersFromDict(dct)
        pendingLinks.extend(super(Chapter, self).setFromDict(dct))
        return pendingLinks

    def solvePendingLinks(self, pendingLinks):
        ''' Solve object pending links.

        :param pendingLinks: list of pending links.
        '''
        rootChapter= self.getRootChapter()
        if(rootChapter is None):
            rootChapter= self
        missingCodes= list()
        for link in pendingLinks:
            key= link['key']
            obj= link['object']
            value= rootChapter.findPrice(key)
            if(value is None):
                value= rootChapter.BuscaCodigo(key)
            if(value):
                attribute= link['attr']
                if(hasattr(obj, attribute)):
                    setattr(obj, attribute, value)
                else:
                    className= type(self).__name__
                    methodName= sys._getframe(0).f_code.co_name
                    logging.error(className+'.'+methodName+'; attribute: '+attribute+' not found for object: '+str(obj))
            else:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+'; price: \''+key+'\' in object: '+ str(obj)+ ' not found.')
                missingCodes.append((key, link))
        if(len(missingCodes)>0):
            logging.error('Some codes were missing. Exiting')
            sys.exit(1)
        return pendingLinks
    
    def getPrice(self):
        priceSubC= self.subcapitulos.getPrice()
        priceQuant= self.quantities.getPrice()
        factor= self.fr.getProduct()
        return (priceSubC + priceQuant)*factor 
    
    def getRoundedPrice(self):
        retval= self.subcapitulos.getRoundedPrice() + self.quantities.getRoundedPrice()
        retval*= self.fr.getRoundedProduct()
        return retval
    
    def ImprCompLtxMed(self, doc, parentSection, other):
        ''' Compare measurements of both projects and write a report.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        :param other: project to compare with.
        '''
        if parentSection!='root':
            doc.append('\\' + parentSection + '{' + self.getTitle() + '}' + '\n')
        self.quantities.ImprCompLtxMed(os, other.quantities)
        logging.error("aqui 1: " + self.getTitle() + ' ' + self.subcapitulos.size() + u" subcapítulos" + '\n')
        logging.error("aqui 2: " + other.getTitle() + ' ' + other.subcapitulos.size() + u" subcapítulos" + '\n')
        self.subcapitulos.ImprCompLtxMed(os,pylatex_utils.getLatexSection(parentSection), other.subcapitulos)
        
    def writeQuantitiesIntoLatexDocument(self, doc, parentSection):
        ''' Write quantities in the pylatex document argument.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        '''
        if(self.hasQuantities()): # There is something to write.
            sectName= pylatex_utils.getLatexSection(parentSection)
            caption= basic_types.quantitiesCaption
            if(sectName!='part'):
                caption= self.getTitle()
            docPart= pylatex_utils.getPyLatexSection(sectName,caption)
            self.quantities.writeQuantitiesIntoLatexDocument(docPart)
            if(len(self.subcapitulos)>0):
                self.subcapitulos.writeQuantitiesIntoLatexDocument(docPart,sectName)
            doc.append(docPart)
        
    def writePriceTableOneIntoLatexDocument(self, doc, parentSection, filterBy= None):
        ''' Write price table number one in the pylatex document argument.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        :param filterBy: write those prices only.
        '''
        if(self.TieneDescompuestos(filterBy= filterBy)):
            if parentSection!='root':
                doc.append('\\' + parentSection + '{' + self.getTitle() + '}' + '\n')
            if self.precios.TieneDescompuestos(filterBy= filterBy):
                self.precios.writePriceTableOneIntoLatexDocument(doc, filterBy= filterBy)
            self.subcapitulos.writePriceTableOneIntoLatexDocument(doc,pylatex_utils.getLatexSection(parentSection), filterBy= filterBy)
            
    def writePriceTableTwoIntoLatexDocument(self, doc, parentSection, filterBy= None):
        ''' Write price table number two in the pylatex document argument.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        :param filterBy: write those prices only.
        '''
        if self.precios.TieneDescompuestos(filterBy= filterBy):
            if parentSection!='root':
                doc.append('\\' + parentSection + '{' + self.getTitle() + '}' + '\n')
            self.precios.writePriceTableTwoIntoLatexDocument(doc, filterBy= filterBy)
        self.subcapitulos.writePriceTableTwoIntoLatexDocument(doc,pylatex_utils.getLatexSection(parentSection), filterBy= filterBy)

    def writeElementaryPrices(self, doc, parentSection, tipos=  [basic_types.mdo, basic_types.maq, basic_types.mat], filterBy= None):
        ''' Write the elementary prices table.

        :param doc: pylatex document to write into.
        :param parentSection: section command for the parent chapter.
        :param tipos: types of the prices to write (maquinaria, materiales o mano de obra) defaults to all of them.
        :param filterBy: write those prices only.
        '''
        if(self.TieneElementales(filterBy= filterBy)):
            if(parentSection!='root'):
                doc.append('\\' + parentSection + '{' + self.getTitle() + '}' + '\n')
            self.precios.writeElementaryPrices(doc, tipos, filterBy= filterBy)
            self.subcapitulos.writeElementaryPrices(doc, pylatex_utils.getLatexSection(parentSection), filterBy= filterBy)
    
    def writePriceJustification(self, doc, parentSection, filterBy= None):
        ''' Write price justification table in the pylatex document argument.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        :param filterBy: write price justification for those prices only.
        :returns: list of the written prices.
        '''
        retval= list()
        if(self.TieneDescompuestos(filterBy= filterBy)):
            if(parentSection!='root'):
                doc.append('\\' + parentSection + '{' + self.getTitle() + '}' + '\n')
            retval= self.precios.writePriceJustification(doc, filterBy= filterBy)
            retval+= self.subcapitulos.writePriceJustification(doc, pylatex_utils.getLatexSection(parentSection), filterBy= filterBy)
        return retval
        
    def ImprLtxResumen(self, doc, parentSection, recursive= True):
        ''' Write a summary report.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        :param recursive: if true apply recursion through chapters.
        '''
        if(self.hasQuantities()):
            if(parentSection!='root'):
                doc.add_item(self.getTitle())
                doc.append(pylatex.Command('dotfill'))
                doc.append(self.getLtxPriceString())
            else:
                doc.append(pylatex_utils.LargeCommand())
                doc.append(pylatex.utils.bold('Total'))
                doc.append(pylatex.Command('dotfill'))
                doc.append(pylatex.utils.bold(self.getLtxPriceString()))
                doc.append(pylatex_utils.NormalSizeCommand())
            if(recursive):
                self.subcapitulos.ImprLtxResumen(doc,pylatex_utils.getLatexSection(parentSection),recursive)
                
    def ImprCompLtxPre(self, doc, parentSection, other):
        ''' Write a comparison report.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        :param other: project to compare with.
        '''
        if parentSection!='root':
            doc.append('\\' + parentSection + '{' + self.getTitle() + '}' + '\n')
        self.quantities.ImprCompLtxPre(doc, self.getTitle(),other.quantities,other.getTitle())
        self.subcapitulos.ImprCompLtxPre(doc,pylatex_utils.getLatexSection(parentSection), other.subcapitulos)
        if self.subcapitulos:
            doc.append(pylatex_utils.ltx_beg_itemize + '\n')
            doc.append("\\item \\noindent \\textbf{Total " + self.getTitle()
               + " (P. de construcción): } \\dotfill \\textbf{"
               + other.getLtxPriceString() + "} " + '\n' + '\n')
            doc.append("\\item \\noindent \\textbf{Total " + self.getTitle()
               + " (P. modificado): }\\dotfill \\textbf{"
               + self.getLtxPriceString() + "} " + '\n')
            doc.append(pylatex_utils.ltx_end_itemize + '\n')
            doc.append("\\clearpage" + '\n')

        if self.quantities:
            doc.append("\\newpage" + '\n')
            
    def hasQuantities(self):
        '''Returns true if the chapter (or its subchapters) have
           quantities.'''
        if(len(self.quantities)):
            return True
        else:
            return self.subcapitulos.hasQuantities()
        
    def setOwner(self, parent):
        if(len(self.subcapitulos)>0):
            self.subcapitulos.setOwner(parent= self)
        if(not self.isRootChapter()):
            self.owner= parent
            
    def findDepth(self):
        ''' Return the height of the chapter tree.'''
        if(self.isRootChapter()):
            retval= 0
        else:
            if(self.owner):
                retval= self.owner.findDepth()+1
            else:
                retval= 0
        return retval
    
    def getHeight(self):
        ''' Return the height of the tree.'''
        retval= self.findDepth()
        if(len(self.subcapitulos)>0):
            depths= self.subcapitulos.getHeights()
            retval= max(retval, max(depths))
        return retval

    def getRootChapter(self):
        ''' Return the root of the chapter three.'''
        if(self.isRootChapter()):
            retval= self
        else:
            if(self.owner):
                retval= self.owner.getRootChapter()
            else:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; chapter: "+str(self.codigo)+' has no owner.')
                retval= None
        return retval
        
    def writePartialBudgetsIntoLatexDocument(self, doc, parentSection):
        '''Write partial budgets in the pylatex document argument.

        :param doc: document to write into.
        :param parentSection: section command for the parent chapter.
        '''
        if(self.hasQuantities()): # There is something to write.
            sectName= pylatex_utils.getLatexSection(parentSection)
            caption= basic_types.partialBudgetsCaption
            if(sectName!='part'):
                caption= self.getTitle()
            docPart= pylatex_utils.getPyLatexSection(sectName,caption)
            self.quantities.writePartialBudgetsIntoLatexDocument(docPart,self.getTitle())
            if(len(self.subcapitulos)>0):
                self.subcapitulos.writePartialBudgetsIntoLatexDocument(docPart, sectName)
                docPart.append(pylatex.Command('noindent'))
                docPart.append(pylatex_utils.largeCommand())
                docPart.append(pylatex.utils.bold('Total: '+self.getTitle()+' '))
                docPart.append(pylatex.Command('dotfill'))
                docPart.append(pylatex.utils.bold(self.getLtxPriceString()))
                docPart.append(pylatex.NewLine())
                docPart.append(pylatex_utils.NormalSizeCommand())
            doc.append(docPart)
            
    def writeSpreadsheetSummary(self, sheet, depth, maxDepth, recursive= True):
        ''' Write a summary report.

        :param sheet: spreadsheet to write into.
        :param parentSection: section command for the parent chapter.
        :param recursive: if true apply recursion through chapters.
        '''
        if(self.hasQuantities() and depth<=maxDepth):
            row= (maxDepth+3)*[None]
            row[depth]= self.getTitle()
            row[-1]= self.getPrice()
            sheet.row+= row
            if(recursive):
                self.subcapitulos.writeSpreadsheetSummary(sheet, depth= depth+1, recursive= recursive, maxDepth= maxDepth)

    def writeSpreadsheetQuantities(self, sheet, parentSection):
        ''' Write the quantities in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        :param parentSection: name of the parent section.
        '''
        sheet.row+= [self.getTitle()]
        self.quantities.writeSpreadsheetQuantities(sheet)
        self.subcapitulos.writeSpreadsheetQuantities(sheet, parentSection)

    def writeSpreadsheetBudget(self, sheet, parentSection):
        ''' Write the budget in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        :param parentSection: name of the parent section.
        '''
        sheet.row+= [self.getTitle()]
        self.quantities.writeSpreadsheetBudget(sheet)
        sheet.row+= [None, None, None, None,"Total: ",self.getTitle(),None,self.getPriceString()]
        sheet.row+= [None]
        self.subcapitulos.writeSpreadsheetBudget(sheet,parentSection)

    def getQuantitiesReport(self):
        ''' Return a report containing the total measurement for 
            each unit price.'''
        retval= self.quantities.getQuantitiesReport()
        retval.Merge(self.subcapitulos.getQuantitiesReport())
        return retval

    def getEmployedPrices(self, lowerMeasurementBound= 0.0):
        ''' Return the codes of the prices that have a total measurement
            greater than the limit argument.

        :param lowerMeasurementBound: lower bound for the total measurement.
        '''
        quantitiesReport= self.getQuantitiesReport()
        return quantitiesReport.getKeysWithMeasurementGreaterThan(lowerMeasurementBound= lowerMeasurementBound)

    def getEmployedElementaryPrices(self, lowerMeasurementBound= 0.0):
        ''' Return the codes of the elementary prices that have a total 
            measurement greater than the limit argument.

        :param lowerMeasurementBound: lower bound for the total measurement.
        '''
        employedPrices= self.getEmployedPrices(lowerMeasurementBound= lowerMeasurementBound)
        retval= set()
        for key in employedPrices:
            price= self.findPrice(key)
            if(hasattr(price, 'components')): # is a compound price
                for c in price.components:
                    code= c.CodigoEntidad()
                    retval.add(code)
            else: # it's an elementary price already.
                retval.add(key)
        return retval
       
    def writeMembersToJSON(self, outputFileName, indent= 2):
        ''' Write data to a JSON file.

        :param outputFileName: name of the output file.
        '''
        # Write data to file.
        outputFile= open(outputFileName, mode='w')
        outputs= json.dump(self.getMembersDict(), outputFile, indent= indent)
        outputFile.close()
        
    def readMembersFromJSON(self, inputFileName):
        ''' Read member data from a JSON file.

        :param inputFileName: name of the output file.
        '''
        # Read data from file.
        inputFile= open(inputFileName, mode='r')
        dataDict= json.load(inputFile)
        inputFile.close()
        pendingLinks= self.solvePendingLinks(self.setMembersFromDict(dataDict))
        return pendingLinks
        
    def readFromJson(self, inputFileName):
        ''' Load data from a JSON file.

        :param inputFileName: name of the input file.
        '''
        # Read data from file.
        inputFile= open(inputFileName, mode='r')
        dataDict= json.load(inputFile)
        inputFile.close()
        pendingLinks= self.solvePendingLinks(self.setFromDict(dataDict))
        return pendingLinks
        
    def writeJson(self, outputFileName, indent= 2):
        ''' Write data to a JSON file.

        :param outputFileName: name of the output file.
        '''
        # Write data to file.
        outputFile= open(outputFileName, mode='w')
        outputs= json.dump(self.getDict(), outputFile, indent= indent)
        outputFile.close()
        
    def clear(self):
        '''removes all items from the chapter.'''
        self.quantities.clear()
        self.subcapitulos.clear()
        self.precios.clear()
