# -*- coding: utf-8 -*-
''' Unit price.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import pylatex
import logging
from pycost.utils import measurable as ms
from pycost.prices import elementary_price_container
from pycost.prices import component_list
from pycost.utils import pylatex_utils
from pycost.utils import basic_types
from pycost.bc3 import fr_entity
from pycost.bc3 import bc3_component
from decimal import Decimal

class UnitPrice(ms.Measurable):
    ''' Cost of the materials, equipment, and labor needed
        to build a building unit.

    :ivar components: components of the cost (materials,...).
    '''
    precision= 2
    places= Decimal(10) ** -precision
    formatString= '{0:.'+str(precision)+'f}'
    descriptionColumnWidth= 60 # Width of the description column in mm.

    def __init__(self, cod="", desc="", ud="", ld= None):
        ''' Constructor.
 
        :param cod: identifier.
        :param tit: short description.
        :param ud: unit of measurement.
        :param ld: long description.
        '''
        super(UnitPrice,self).__init__(cod= cod, tit= desc, ud= ud, ld= ld)
        self.components= component_list.ComponentList()
        
    def getType(self):
        return 0

    def isCompound(self):
        ''' Return true if it is a compound concept instead of a simple one.'''
        return True
    
    def dependsOnConcept(self,  priceCode):
        ''' Return the prices which depend on the one whose code
            is passed as parameter.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        return self.components.dependsOnConcept(priceCode)

    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        self.components.removeConcept(conceptToRemoveCode)
                
    def replaceConcept(self, oldPriceCode, newPrice):
        ''' Return the prices which depend on the one whose code
            is passed as parameter.

        :param oldPriceCode: code of the price to replace.
        :param newPrice: replacement price (not the code, the object).
        '''
        return self.components.replaceConcept(oldPriceCode, newPrice)
    
    def getElementaryComponentFactors(self, parentPrices, parentFactor= 1.0):
        ''' Return the factors of the elementary components of this 
            collection (if any component is composed append its 
            decomposition to the returned container).

        :param parentPrices: chain of prices that contains this one.
        :param parentFactor: factor from the upper call.
        '''
        return self.components.getElementaryComponentFactors(parentPrices= parentPrices, parentFactor= parentFactor)

    def getElementaryComponents(self, parentPrices, parentFactor= 1.0):
        ''' Return the elementary components of this price.

        :param parentPrices: chain of prices that contains this one.
        :param previousComponents: dictionary containing the components already
                                   obtained.
        '''
        code= self.Codigo()
        retval= self.components.getElementaryComponents(parentPrices= parentPrices, parentFactor= parentFactor)
        for key in retval:
            c= retval[key]
        return retval

    def getNumberOfWorkers(self):
        ''' Return the number of workers needed to perform this task.'''
        return self.components.getNumberOfWorkers()
            
    def getPrice(self):
        return self.components.getPrice()

    def AsignaFactor(self, f):
        self.components.AsignaFactor(f)

    def Append(self,entity, f, r):
        tmp= bc3_component.BC3Component(e= entity,fr= fr_entity.EntFR(f,r))
        self.components.append(tmp)
        return tmp

    def LeeBC3Fase1(self,r):
        '''Lee la unidad a falta de la descomposición.'''
        super(UnitPrice,self).readBC3(r)

    def LeeBC3Fase2(self, r, rootChapter):
        ''' Read the components of the unit.

        :param rootChapter: root chapter (access to the already 
                            defined concepts).
        '''
        error= False
        if(len(r.Datos().desc)>0):
            tmp= UnitPrice.getPointers(r.Datos().desc, error, rootChapter= rootChapter)
            if not error:
                self.components= tmp
            else:
                logging.error("Error reading components of unit: " + self.Codigo() + '\n')

        else:
            self.components= self.GetSindesco(r.Datos().getPrice(),rootChapter.precios)
        return error

    def GetSindesco(self, productionRate, bp):
        '''Para unidades de obra sin descomposición de las que
           sólo se conoce el precio.

        :param productionRate: production rate.
        :param bp: price dictionary.
        '''
        retval= component_list.ComponentList()
        be= bp.elementos
        ent= be.Busca("SINDESCO")
        factorAndRate= fr_entity.EntFR(1.0,productionRate)
        retval.append(bc3_component.BC3Component(e= ent,fr= factorAndRate))
        return retval

    @staticmethod
    def getPointers(descBC3, error, rootChapter):
        '''Get the pointers to the component prices.

        :param rootChapter: root chapter (access to the already 
                            defined concepts).
        '''
        retval= component_list.ComponentList()
        ent= None
        for i in descBC3:
            ent= rootChapter.getUnitPrice((i).codigo)
            if not ent:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.warning(className+'.'+methodName+"; component: " + (i).codigo + 'not found.')
                error= True
                continue
            else:
                retval.append(bc3_component.BC3Component(ent,i))
                error= False
        return retval

    def WriteSpre(self, os):
        os.write(self.Codigo() + '|'
           + self.Unidad() + '|'
           + getTitle() + '|')
        self.components.WriteSpre(os)

    def WriteBC3(self, os):
        super(UnitPrice,self).WriteBC3(os)
        self.components.WriteBC3(self.Codigo(),os)


    def Write(self, os= sys.stdout):
        super(UnitPrice,self).Write(os)
        self.components.Write(os)
        
    def SimulaDescomp(self,otra):
        '''Toma la descomposición de otra unidad de obra.
           sin alterar el precio de ésta.'''
        objetivo= self.getPrice()
        self.components= copia(otra.components)
        return self.components.FuerzaPrecio(objetivo)

    @staticmethod
    def getJustificationTableLtxTableSpec():
        ''' Return the table spec for the justification table.'''
        return  'l r l p{'+str(UnitPrice.descriptionColumnWidth)+'mm} r r'

    def populateJustificationTable(self, data_table):
        ''' Populate the given table with the price justification data.

        :param data_table: pylatex tabular data to populate.
        '''
        unitDescriptionWidth= UnitPrice.descriptionColumnWidth+35
        row= [pylatex_utils.ascii2latex(self.Codigo())]
        row.append(pylatex_utils.ascii2latex(self.Unidad()))
        row.append(pylatex.table.MultiColumn(4, align=pylatex.utils.NoEscape('p{'+str(unitDescriptionWidth)+'mm}'),data=pylatex_utils.ascii2latex(self.getNoEmptyDescription())))
        data_table.add_row(row)
        # Header
        headerRow= [u'Código',u'Rdto.',u'Ud.',u'Descripción',u'Unit.',u'Total']
        data_table.add_row(headerRow)
        data_table.add_hline()
        # Decomposition
        self.components.writePriceJustification(data_table, pa= True); # Cumulated percentages.
        
    def writePriceJustification(self, data_table, use_nested_table):
        ''' Write price justification in the table argument.

        :param data_table: pylatex tabular data to populate.
        :param use_nested_table: if true use a nested table that is inserted
                                 in the given one.
        '''
        tableStr= UnitPrice.getJustificationTableLtxTableSpec()
        if(use_nested_table):
            nested_data_table= pylatex.Tabular(tableStr)
            self.populateJustificationTable(nested_data_table)
            data_table.add_row([nested_data_table])
        else:
            self.populateJustificationTable(data_table)
            data_table.add_empty_row()

    def getLtxCodeUnitDescription(self):
        retval= [pylatex_utils.ascii2latex(self.Codigo())]
        retval.append(pylatex_utils.ascii2latex(self.Unidad()))
        retval.append(pylatex_utils.ascii2latex(self.getNoEmptyDescription()))
        return retval

    def writePriceTableOneIntoLatexDocument(self, data_table):
        '''Write first price table.

        :param data_table: pylatex table to write into.
        '''
        row= self.getLtxCodeUnitDescription()
        row.extend(['',''])
        data_table.add_row(row)
        self.components.writePriceTableOneIntoLatexDocument(data_table,True,False); #XXX Aqui género.

    def writePriceTableTwoIntoLatexDocument(self, data_table):
        '''Write second price table.

        :param data_table: pylatex table to write into.
        '''
        tableStr= 'l r p{5.5cm} r'
        headerRow= [u'Código',u'Ud.',u'Descripción',u'Importe']
        nested_data_table= pylatex.Tabular(tableStr)
        # Header
        nested_data_table.add_row(headerRow)
        nested_data_table.add_hline()
        row= self.getLtxCodeUnitDescription()
        row.append('')
        nested_data_table.add_row(row)
        # Decomposition
        self.components.writePriceTableTwoIntoLatexDocument(nested_data_table,True); #XXX Here cumulated percentages.
        data_table.add_row([nested_data_table])

    def writeSpreadsheet(self, sheet):
        sheet.append([self.Codigo(), pylatex_utils.ascii2latex(self.Unidad()),pylatex_utils.ascii2latex(self.getNoEmptyDescription()),self.StrPriceToWords(True) ,self.getPriceString()])

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(UnitPrice, self).getDict()
        retval['components']= self.components.getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        if('components' in dct):
            pendingLinks= self.components.setFromDict(dct['components']) # Links that cannot be set yet.
        else:
            logging.error("'components' key missing in input dictionary:"+str(dct))
            exit(-1)
        pendingLinks.extend(super(UnitPrice, self).setFromDict(dct))
        return pendingLinks

    def appendToChapter(self, chapter):
        ''' Insert this price in the chapter argument.'''
        for comp in self.components:
            comp.ent.appendToChapter(chapter)
        chapter.precios.unidades.Append(self)
