# -*- coding: utf-8 -*-
''' Price tables.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pycost.prices import elementary_price_container
from pycost.prices import unit_price_container
from pycost.bc3 import codigos_obra
from pycost.utils import EntPyCost as epc
from pycost.utils import basic_types

class CuaPre(epc.EntPyCost):
    ''' Price tables:

    :ivar elementos: elementary prices.
    :ivar unidades: composed prices.
    '''
    def __init__(self):
        super(CuaPre,self).__init__()
        self.elementos= elementary_price_container.ElementaryPrices() #Precios elementales.
        self.unidades= unit_price_container.Descompuestos() #Unidades de obra.

    def Elementales(self):
        ''' Return the container of the elementary prices.'''
        return self.elementos

    def UdsObra(self):
        ''' Return the container of the compount prices.'''
        return self.unidades

    def NumElementales(self, filterBy= None):
        ''' Return the number of elementary prices. If filterBy is not None
        return only the number of elementary prices whose code is also in the
        filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        return self.elementos.size(filterBy= filterBy)                
    
    def TieneElementales(self, filterBy= None):
        ''' Return true if the container has elementary prices. If filterBy 
        is not None return true only if the number of elementary prices 
        whose code is also in the filterBy list is not zero.

        :param filterBy: count only the codes on this list.
        '''
        
        return (self.NumElementales(filterBy= filterBy)>0)

    def newElementaryPrice(self, code, shortDescription, price, typ, unit, longDescription= None):
        ''' Define an elementary price.

        :param code: price identifier.
        :param shortDescription: short description of the price.
        :param typ: price type (labor, machinery, materials or unclassified).
        :param unit: unit (m, kg,...).
        :param longDescription: long description of the price.
        '''
        return self.elementos.newElementaryPrice(code= code, shortDescription= shortDescription, price= price, typ= typ, unit= unit, longDescription= longDescription)
        
    def NumDescompuestos(self, filterBy= None):
        ''' Return the number of compound prices. If filterBy is not None
        return only the number of compound prices whose code is also in the
        filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        return self.unidades.size(filterBy= filterBy)
    
    def newCompoundPrice(self, code, shortDescription, components, unit, longDescription= None):
        ''' Define a compount price.

        :param code: price identifier.
        :param shortDescription: short description of the price.
        :param components: price decomposition.
        :param unit: unit (m, kg,...).
        :param longDescription: long description of the price.
        '''
        return self.unidades.newCompoundPrice(code= code, shortDescription= shortDescription, components= components, unit= unit, longDescription= longDescription)

    def TieneDescompuestos(self, filterBy= None):
        return (self.NumDescompuestos(filterBy= filterBy)>0)

    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        self.unidades.removeConcept(conceptToRemoveCode)
        self.elementos.removeConcept(conceptToRemoveCode)

    def getConceptsThatDependOn(self, priceCode):
        ''' Return the prices which depend on the one whose code
            is passed as parameter.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        # Elementary prices doesn't depend on anything.
        return self.unidades.getConceptsThatDependOn(priceCode)
        
    
    def appendComponent(self, cod_ud, cod_el, r, f= 1.0):
        self.unidades.appendComponent(elementos,cod_ud,cod_el,r,f)

    def LeeBC3Elementales(self, elem):
        ''' Read elementary prices.'''
        self.elementos.readBC3(elem)

    def LeeBC3DescompFase1(self, descomp):
        self.unidades.LeeBC3Fase1(descomp)

    def LeeBC3DescompFase2(self, descomp, rootChapter):
        return self.unidades.LeeBC3Fase2(descomp, rootChapter= rootChapter)

    def searchForUnitPrice(self, cod):
        return self.unidades.Busca(cod)

    def BuscaElementaryPrice(self, cod):
        return self.elementos.Busca(cod)

    def findPrice(self, cod):
        ''' Return the concept with the code corresponding to the argument.

        :param cod: code of the concept to find.
        '''
        retval= self.searchForUnitPrice(cod)
        if not retval:
            retval= self.BuscaElementaryPrice(cod)
        return retval
    
    def findPricesRegex(self, regex):
        ''' Return the concepts with a code that matches to the regular
            expression argument.

        :param regex: regular expression to match with the concept code.
        '''
        retval= self.unidades.findRegex(regex)
        retval.extend(self.elementos.findRegex(regex))
        return retval

    def WriteSpre(self):
        self.elementos.WriteSpre()
        ofs_des= std.ofstream("DES001.std",std.ios.out)
        self.unidades.WriteSpre(ofs_des)
        ofs_des.close()

    def WriteBC3(self, os):
        self.elementos.WriteBC3(os)
        self.unidades.WriteBC3(os)

    def LeeSpre(self, iS):
        self.elementos.LeeSpre(iS)
        Str=''
        getline(iS,Str,'\n')
        if(Str.find("[DES]")<len(Str)):
            self.unidades.LeeSpre(iS,elementos)


    def writeElementaryPrices(self, doc, tipos=  [basic_types.mdo, basic_types.maq, basic_types.mat], filterBy= None, superTabular= False):
        ''' Write the elementary prices table.

        :param doc: pylatex document to write into.
        :param tipos: types of the prices to write (maquinaria, materiales o mano de obra) defaults to all of them.
        :param filterBy: write those prices only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        self.elementos.writeLatex(doc, tipos, filterBy= filterBy, superTabular= superTabular)

    def writePriceJustification(self, doc, filterBy= None, superTabular= False):
        '''Write price justification.

        :param doc: pylatex document to write into.
        :param filterBy: write price justification for those prices only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        :returns: list of the written prices.
        '''
        return self.unidades.writePriceJustification(doc, filterBy= filterBy, superTabular= superTabular)


    def writePriceTableOneIntoLatexDocument(self, doc, filterBy= None, superTabular= False):
        '''Write first price table.

        :param doc: pylatex document to write into.
        :param filterBy: write price only if its code is in the list.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        self.unidades.writePriceTableOneIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular)

    def writePriceTableTwoIntoLatexDocument(self, doc, filterBy= None, superTabular= False):
        '''Write second prince table.

        :param doc: pylatex document to write into.
        :param filterBy: write price only if its code is in the list.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        self.unidades.writePriceTableTwoIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular)

    def writePriceTablesIntoLatexDocument(self, doc, filterBy= None, superTabular= False):
        '''Write both price tables.

        :param doc: pylatex document to write into.
        :param filterBy: write price only if its code is in the list.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        writePriceTableOneIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular)
        writePriceTableTwoIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular)

    def writeSpreadsheet(self, book):
        ''' Write the prices in the work book argument.

        :param book: spreadsheet book.
        '''
        self.elementos.writeSpreadsheet(book['Elementales'])
        self.unidades.writeSpreadsheet(book['CuaPre1'])

    def SimulaDescomp(self, origen, destino):
        self.unidades.SimulaDescomp(origen,destino)

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(CuaPre, self).getDict()
        retval['elementary_prices']= self.elementos.getDict()
        retval['units']= self.unidades.getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        # pendingLinks: links that cannot be set yet.
        pendingLinks= self.elementos.setFromDict(dct['elementary_prices'])
        pendingLinks.extend(self.unidades.setFromDict(dct['units']))
        pendingLinks.extend(super(CuaPre, self).setFromDict(dct))
        return pendingLinks

    def clear(self):
        '''removes all items from the chapter.'''
        self.unidades.clear()
        self.elementos.clear()
        
