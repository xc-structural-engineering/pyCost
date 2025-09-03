# -*- coding: utf-8 -*-
''' Unit price container.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
import logging
import sys
import difflib
from pycost.prices import elementary_price_container
from pycost.prices import unit_price
from pycost.prices import parametric
from pycost.utils import concept_dict
from pycost.utils import pylatex_utils

class Descompuestos(concept_dict.ConceptDict):
    '''Unidades de obra.

    :ivar parametricConcepts: parametric concepts dictionary.
    '''
    def __init__(self):
        super().__init__()
        self.parametricConcepts= dict()

    def size(self, filterBy= None):
        ''' Return the number of compound prices in this container. If 
        filterBy is not None return only the number of compound prices 
        whose code is also in the filterBy list.

        :param filterBy: count only if the code is in this list.
        '''
        retval= len(self)
        if(filterBy is not None):
            retval= 0
            for key in self.concepts:
                if key in filterBy:
                    retval+= 1
        return retval
    
    def newCompoundPrice(self, code, shortDescription, components, unit, longDescription= None):
        ''' Define a compount price.

        :param code: price identifier.
        :param shortDescription: short description of the price.
        :param components: price decomposition.
        :param unit: unit (m, kg,...).
        :param longDescription: long description of the price.
        '''
        if(code in self.concepts):
            logging.warning('Code: '+code+' already exists in the price table.')
        newPrice= unit_price.UnitPrice(cod= code, desc= shortDescription, ud= unit, ld= longDescription)
        newPrice.components.setFromTupleList(components)
        self.Append(newPrice)
        return newPrice
    
    def appendComponent(self, el, cod_ud, cod_el, r, f):
        ''' Append a new component to the container.

        :param el: elementary prices container.
        :param cod_ud: unit price 
        '''
        i= self.Busca(cod_ud)
        j= el.Busca(cod_el)
        if not j:
            logging.error("Elemento: " + cod_el
                      + " no encontrado en unidad de obra: " + cod_ud + '\n')
            exit(1)

        i.Append(j,f,r)

    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        for key in self.concepts:
            concept= self.concepts[key]
            if(concept.dependsOnConcept(conceptToRemoveCode)):
                concept.removeConcept(conceptToRemoveCode)

    def getConceptsThatDependOn(self, priceCode):
        ''' Return the prices which depend on the one whose code
            is passed as parameter.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        retval= list()
        for key in self.concepts:
            concept= self.concepts[key]
            if(concept.dependsOnConcept(priceCode)):
                retval.append(concept)
        return retval

    def LeeBC3Fase1(self, cds):
        '''Read the units whitout its components.'''
        for key in cds:
            if('$' in key): # parametric concept.
                reg= cds.getParametricData(key)
                self.parametricConcepts[key]= parametric.Parametric(c= reg.datos.concept, t= reg.datos.txt, p= reg.datos.parameters)
            else: # not a parametric concept.
                reg= cds.getUnitPriceData(key)
                ud= unit_price.UnitPrice()
                ud.LeeBC3Fase1(reg)
                self.Append(ud)

    def LeeBC3Fase2(self, cds, rootChapter):
        '''Reads the components of the unit.'''
        ud= None
        error= False
        retval= set()
        for key in cds:
            if(not '$' in key): # not a parametric concept.
                reg= cds.getUnitPriceData(key)
                ud= self.Busca(reg.Codigo())
                error= ud.LeeBC3Fase2(reg, rootChapter= rootChapter)
                if error:
                    retval.add(reg.Codigo())
        return retval

    def WriteSpre(self, os):
        for j in self.concepts:
            self.concepts[j].WriteSpre(os)

    def AsignaFactor(self, f):
        for j in self.concepts:
            self.concepts[j].AsignaFactor(f)

    def LeeSpre(self, iS, elementos):
        if iS.peek()!= 26:
            while(True):
                cod= ''
                getline(iS,cod,'|')
                ud= ''
                getline(iS,ud,'|')
                if ud.find('%')<len(ud):
                    cod= "%" + cod
                    ud= ""

                tit= ''
                getline(iS,tit,'|')
                unidad= UnitPrice(cod,tit,ud)
                unidad.texto_largo= tit
                self.Append(unidad)
                perc= '' #percentage
                getline(iS,perc,'|')
                descomp= '' #descomposición
                getline(iS,descomp,'\n')
                #istrstream istr(descomp.c_str(),descomp.leng.py())
                while(True):
                    pos2= descomp.find('|')
                    cod_el= descomp.substr(0,pos2)
                    descomp.replace(0,pos2+1,"")
                    pos3= descomp.find('|')
                    cantidad= ''
                    if pos3<1000:
                        cantidad= descomp.substr(0,pos3)
                        descomp.replace(0,pos3+1,"")
                    else:
                        cantidad= descomp.substr(0,len(descomp)-1)
                    if(elementos.find("%" + cod_el)!=elementos.end()): #Corresponds to a percentage.
                        cod_el= "%"+cod_el
                    appendComponent(el= elementos, cod_ud= cod, cod_el= cod_el, r= atof(cantidad.c_str()))
                    if(pos3>len(descomp)): break

                if(iS.peek() == 26): break

        resto= ''
        getline(iS,resto,'\n')

    def filterConcepts(self, filterBy= None):
        ''' Return a list with the concepts filtered by the list argument.

        :param filterBy: return the prices whose code is in the list only.
        '''
        retval= list()
        if(filterBy is None):
            retval= list(self.concepts.keys())
        else:
            for key in self.concepts:
                if(key in filterBy):
                    retval.append(key)
        return retval
        
    def writePriceTableOneIntoLatexDocument(self, doc, filterBy= None):
        ''' Write unit price table one into a latex report.

        :param doc: pylatex document to write into.
        :param filterBy: write price table for those prices only.
        '''
        if(len(self)>=1):
            num_campos= 5
            doc.append(pylatex_utils.SmallCommand())
            longTableStr= '|l|l|p{4cm}|p{3cm}|r|'
            headerRow1= [u'Código','Ud.',u'Denominación',(pylatex.table.MultiColumn(2,align='|c|',data= 'Precio'))]
            headerRow2= ['','','','en letra', 'en cifra']
            with doc.create(pylatex_utils.LongTable(longTableStr)) as data_table:
                data_table.add_hline()
                data_table.add_row(headerRow1)
                data_table.add_row(headerRow2)
                data_table.add_hline()
                data_table.end_table_header()
                data_table.add_hline()
                data_table.add_row((pylatex.table.MultiColumn(num_campos, align='|r|',data='../..'),))
                data_table.add_hline()
                data_table.end_table_footer()
                data_table.add_hline()
                data_table.end_table_last_footer()
                filteredConcepts= self.filterConcepts(filterBy= filterBy)
                for key in sorted(filteredConcepts):
                    data_table.add_empty_row()
                    self.concepts[key].writePriceTableOneIntoLatexDocument(data_table)
                    data_table.add_empty_row()

            doc.append(pylatex_utils.NormalSizeCommand())

    def writePriceJustification(self, doc, filterBy= None):
        ''' Write price justification into a latex report.

        :param doc: pylatex document to write into.
        :param filterBy: write price justification for those prices only.
        :returns: list of the written prices.
        '''
        retval= list()
        if(len(self)>0):
            filteredConcepts= self.filterConcepts(filterBy= filterBy)
            if(len(filteredConcepts)>0):
                doc.append(pylatex_utils.SmallCommand())
                longTableStr= 'l'
                with doc.create(pylatex_utils.LongTable(longTableStr)) as data_table:
                    for key in sorted(filteredConcepts):
                        self.concepts[key].writePriceJustification(data_table)
                        retval.append(key)
                doc.append(pylatex_utils.NormalSizeCommand())
        return retval

    def writePriceTableTwoIntoLatexDocument(self, doc, filterBy= None):
        ''' Write unit price table two into a latex report.

        :param doc: pylatex document to write into.
        :param filterBy: write price table for those prices only.
        '''
        if(len(self)>0):
            #doc.append(pylatex_utils.ltx_star_.chapter("Cuadro de precios no. 2") + '\n'
            doc.append(pylatex_utils.SmallCommand())
            longTableStr= 'l'
            with doc.create(pylatex_utils.LongTable(longTableStr)) as data_table:
                filteredConcepts= self.filterConcepts(filterBy= filterBy)
                for key in sorted(filteredConcepts):
                    self.concepts[key].writePriceTableTwoIntoLatexDocument(data_table)
            doc.append(pylatex_utils.NormalSizeCommand())

    def writeSpreadsheet(self, sheet):
        sheet.append([u"Código", "Ud.", "Denominación", "Precio en letra", "Precio en cifra"])
        for j in self.concepts:
            self.concepts[j].writeSpreadsheet(sheet)

    def getParametricConceptsKeys(self):
        ''' Return the keys of the parametric concepts.'''
        return list(self.parametricConcepts.keys())

    def getParametricConcept(self, key):
        ''' Return the parametric concept identified by the key.'''
        retval= None
        if key in self.parametricConcepts:
            retval= self.parametricConcepts[key]
        else:
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            logging.error(className+'.'+methodName+'; parametric concept: \''+str(key)+'\' not found. Candidates are:')
            candidate_keys= self.parametricConcepts.keys()
            if(len(candidate_keys)>10): # Do not fill the console with data.
                candidate_keys= difflib.get_close_matches(key, candidate_keys)
            logging.error(str(candidate_keys))
        return retval

    def writeParametricConcepts(self, os= sys.stdout):
        ''' Writes a report of the parametrics concepts.'''
        for key in self.parametricConcepts:
            pc= self.parametricConcepts[key]
            pc.Write(os)
            
    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= dict()
        # Populate with regular unit prices.
        regularDict= super(Descompuestos, self).getDict()
        retval['regular']= regularDict
        # Populate with parametric unit prices.
        parametricDict= dict()
        for key in self.parametricConcepts:
            parametricConcept= self.parametricConcepts[key]
            parametricDict[key]= parametricConcept.getDict()
        retval['parametric']= parametricDict
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= list() # Links that cannot be set yet.
        # Read regular unit prices.
        if('regular' in dct):
            regularDict= dct['regular']
            if(regularDict):
                for key in regularDict:
                    p= unit_price.UnitPrice(key)
                    itemDict= regularDict[key]
                    pendingLinks.extend(p.setFromDict(itemDict))
                    self.Append(p)
                pendingLinks.extend(super(Descompuestos, self).setFromDict(regularDict))
        else:
            logging.info('No regular unit prices.')
        if('parametric' in dct):
            parametricDict= dct['parametric']
            if(parametricDict):
                for key in parametricDict:
                    value= parametricDict[key]
                    param= parametric.Parametric()
                    param.setFromDict(value)
                    self.parametricConcepts[key]= param
        else:
            logging.info('No parametric prices.')
        return pendingLinks

    def clear(self):
        '''removes all items from the container.'''
        # for p in self.concepts:
        #     print('unit price container: ', p)
        #     p.clear()
        super(Descompuestos, self).clear()
        self.parametricConcepts.clear()
