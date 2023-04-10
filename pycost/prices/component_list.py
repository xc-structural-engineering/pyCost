# -*- coding: utf-8 -*-
''' Component list.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import logging
from pycost.utils import EntPyCost as epc
from pycost.prices.price_justification import PriceJustificationList as pjl
from pycost.prices.price_justification import PriceJustificationRecordContainer as pjrc
from pycost.bc3 import bc3_component
from pycost.utils import basic_types

class ComponentList(list, epc.EntPyCost):
    '''Componentes de un precio descompuesto.'''
    
    def __init__(self):
        super(ComponentList,self).__init__()
        epc.EntPyCost.__init__(self)
        
    def getPrice(self):
        return self.getRoundedPrice()

    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        toRemove= list()
        for i in self:
            if(i.CodigoEntidad()==conceptToRemoveCode):
                toRemove.append(i)
        for j in toRemove:
            self.remove(j)
                
    def dependsOnConcept(self, priceCode):
        ''' Return the true if the pric whose code is passed as parameter
        makes part of this component list.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        retval= False
        for i in self:
            if(i.CodigoEntidad()==priceCode):
                retval= True
                break
        return retval
    
    def replaceConcept(self, oldPriceCode, newPrice):
        ''' Return the prices which depend on the one whose code
            is passed as parameter.

        :param oldPriceCode: code of the price to replace.
        :param newPrice: replacement price (not the code, the object).
        '''
        for i in self:
            code= i.CodigoEntidad()
            if(code==oldPriceCode):
                i.ent= newPrice # Replaces the price.
        
    def AsignaFactor(self, f):
        '''Asigna el valor f a los factores de toda la descomposición.'''
        for i in self:
            (i).factor= f

    def WriteSpre(self, os):
        if(len(self)):
            for i in self:
                i.WriteSpre(os)
            os.write('|' + '\n')

    def WriteBC3(self, cod, os):
        if(len(self)):
            os.write("~D" + '|' + cod + '|')
            for i in self:
                i.WriteBC3(os)
            os.write('|' + '\n')

    def Write(self, os= sys.stdout):
        os.write('components: ')
        for c in self:
            c.Write(os)
            os.write('\n')

    def getRoundedPrice(self):
        lista= self.getPriceJustificationList(True)#XXX Here cumulated percentages.
        return basic_types.ppl_price(float(lista.getRoundedTotal()))


    #not  @brief Suma de los precios de un tipo (mdo, maq, mat,...)
    def PrecioPorTipo(self, tipo):
        ptipo= basic_types.ppl_price(0.0) #Total price.
        for i in self:
            if (i).getType()==tipo and not (i).isPercentage():
                ptipo+= (i).getRoundedPrice()
        return ptipo

    def PrecioSobre(self, tipo, sobre):
        '''Computes percentages over a type.'''
        ptipo= basic_types.ppl_price(0.0); #Precio total.
        for i in self: #Percentages.
            if (i).getType()==tipo and (i).isPercentage():
                ptipo+= (i).PrecioSobre(sobre)
        return ptipo

    def SumPercentages(self, tipo):
        porc= 0.0; #Total percentage.
        for i in self: #Percentages.
            if (i).getType()==tipo and (i).isPercentage():
                porc+= (i).getProduct()
        return porc


    def CalculaLambda(self, objetivo):
        sum_porc= SumPercentages(sin_clasif)
        sum_pi= getPrice(mdo)+getPrice(maq)
        pmat= getPrice(mat)
        numerador= objetivo/(1.0+sum_porc)-pmat
        return (numerador/sum_pi)


    def FuerzaPrecio(self, objetivo):
        Lambda= CalculaLambda(objetivo)
        for i in self: #Percentages.
            if(((i).getType()!=mat) and not ((i).isPercentage())):
                i.productionRate*= Lambda
        if Lambda<0.0:
            logging.error("lambda= " + Lambda + " negativo" + '\n')

        return Lambda

    def getElementaryPricesOfType(self, typo):
        lista= pjrc.PriceJustificationRecordContainer(typo)
        for i in self:
            if(i.getType()==typo):
                if not i.isPercentage():
                    lista.append((i).getPriceJustificationRecord(0.0))
        return lista

    def getPourcentagesForType(self, typo):
        lista= pjrc.PriceJustificationRecordContainer(typo)
        for i in self:
            if (i).getType()==typo and (i).isPercentage():
                lista.append((i).getPriceJustificationRecord(0.0))
        return lista


    def getPriceJustificationList(self, pa):
        ''' Return the price justification list.

        :param pa: True percentages must be cumulated.
        '''
        return pjl.PriceJustificationList(pa,self.getElementaryPricesOfType(basic_types.mdo),self.getElementaryPricesOfType(basic_types.mat),self.getElementaryPricesOfType(basic_types.maq),self.getElementaryPricesOfType(basic_types.sin_clasif),self.getPourcentagesForType(basic_types.sin_clasif))


    def writePriceJustification(self, data_table, pa):
        ''' Write the price justification in the argument table.

        :param data_table: LaTeX table to write the justification into.
        :param pa: True percentages must be cumulated.
        '''
        lista= self.getPriceJustificationList(pa)
        lista.writePriceJustification(data_table)

    def writePriceTableTwoIntoLatexDocument(self, os, pa):
        ''' Write the price table number two in LaTeX forma.

        :param os: LaTeX document to write into.
        :param pa: True percentages must be cumulated.
        '''
        lista= self.getPriceJustificationList(pa)
        lista.writePriceTableTwoIntoLatexDocument(os)

    def writePriceTableOneIntoLatexDocument(self, os, pa, gender):
        ''' Write the price table number one in LaTeX forma.

        :param os: LaTeX document to write into.
        :param pa: True percentages must be cumulated.
        :param gender: Gender to use for the currency.
        '''
        lista= self.getPriceJustificationList(pa)
        lista.writePriceTableOneIntoLatexDocument(os,gender)

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= epc.EntPyCost.getDict(self)
        for idx, comp in enumerate(self):
            retval[idx]= comp.getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= list() # Links that cannot be set yet.
        if(isinstance(dct, dict)):
            for key in dct:
                comp= bc3_component.BC3Component(key)
                itemDict= dct[key]
                pendingLinks.extend(comp.setFromDict(itemDict))
                self.append(comp)
            pendingLinks.extend(epc.EntPyCost.setFromDict(self, dct))
        else:
            logging.error('Expected a dictionary, received a: '+str(type(dct))+' with value: '+str(dct))
            exit(1)           
        return pendingLinks

