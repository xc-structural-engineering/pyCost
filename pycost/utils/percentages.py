# -*- coding: utf-8 -*-
''' Percentages.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
from pycost.utils import EntPyCost as epc
from pycost.utils import basic_types
from pycost.utils import pylatex_utils

class Percentages(epc.EntPyCost):
    def __init__(self,gen= 0.17,profit= 0.06,vat= 0.21):
        super(Percentages,self).__init__()
        self.gg= gen #Gastos generales.
        self.bi= profit #Beneficio industrial.
        self.iva= vat #Impuesto sobre el valor añadido.
        
    @staticmethod
    def ApplyPercentage(p, pc):
        temp2= basic_types.ppl_percentage(pc)
        temp3= basic_types.ppl_price(p)
        temp3*=temp2
        return temp3

    def GGenerales(self, p):
        return self.ApplyPercentage(p,self.gg)

    def BIndustrial(self, p):
        return self.ApplyPercentage(p,self.bi)

    def IVA(self, p):
        return self.ApplyPercentage(p,self.iva)

    def getFinalPrices(self, precio_ejec_mat, symbol):
        ''' Return a dictionary containing the prices calculated from the given
            one.

        :param precio_ejec_mat: precio de ejecución material.
        '''
        precision= 2

        retval= dict()
        retval['precio_ejec_mat']= precio_ejec_mat
        retval['precio_ejec_mat_string']= basic_types.human_readable_currency(precio_ejec_mat, symbol= symbol)
        retval['precio_ejec_mat_words']= basic_types.to_words(precio_ejec_mat, False)

        precio_gg= basic_types.ppl_price(self.GGenerales(precio_ejec_mat))
        retval['precio_gg']= precio_gg
        retval['precio_gg_string']= basic_types.human_readable_currency(precio_gg, symbol= symbol)
        precio_bi=  basic_types.ppl_price(self.BIndustrial(precio_ejec_mat))
        retval['precio_bi']= precio_bi
        retval['precio_bi_string']= basic_types.human_readable_currency(precio_bi, symbol= symbol)
        suma_gg_bi= precio_ejec_mat+precio_gg+precio_bi
        retval['suma_gg_bi']= suma_gg_bi
        retval['suma_gg_bi_string']= basic_types.human_readable_currency(suma_gg_bi, symbol= symbol)

        precio_iva= basic_types.ppl_price(self.IVA(suma_gg_bi))
        retval['precio_iva']= precio_iva
        retval['precio_iva_string']= basic_types.human_readable_currency(precio_iva, symbol= symbol)
        
        total= suma_gg_bi + precio_iva
        retval['total']= total
        retval['total_string']= basic_types.human_readable_currency(total, symbol= symbol)
        retval['total_words']= basic_types.to_words(total,False)
        return retval
        

    def printLtx(self, doc, precio_ejec_mat):
        ''' Write in LaTeX format.

        :param doc: pylatex document to write into.
        '''
        precision= 2
        price_data= self.getFinalPrices(precio_ejec_mat, symbol= True)
        precio_ejec_mat_string= price_data['precio_ejec_mat_string']

        # precio_gg= price_data['precio_gg']
        precio_gg_string= price_data['precio_gg_string']

        # precio_bi= price_data['precio_bi']
        precio_bi_string= price_data['precio_bi_string']

        # suma_gg_bi= price_data['suma_gg_bi']
        suma_gg_bi_string= price_data['suma_gg_bi_string']

        # precio_iva= price_data['precio_iva']
        precio_iva_string= price_data['precio_iva_string']
        
        # total= price_data['total']
        total_string= price_data['total_string']
        total_words= price_data['total_words']
        
        with doc.create(pylatex.Itemize()) as itemize:
            itemize.add_item(u'Total presupuesto de ejecución material ')
            itemize.append(pylatex.Command('dotfill'))
            itemize.append(precio_ejec_mat_string)
            
            itemize.add_item(str(self.gg*100) + u'% Gastos generales ')
            itemize.append(pylatex.Command('dotfill'))
            itemize.append(precio_gg_string)
            
            itemize.add_item(str(self.bi*100) + u'% Beneficio industrial ')
            itemize.append(pylatex.Command('dotfill'))
            itemize.append(precio_bi_string)
            
            itemize.add_item('Suma ')
            itemize.append(pylatex.Command('dotfill'))
            itemize.append(suma_gg_bi_string)
            
            itemize.add_item(str(self.iva*100) + u'% I.V.A. ')
            itemize.append(pylatex.Command('dotfill'))
            itemize.append(precio_iva_string)
            
            
        doc.append(pylatex.utils.bold(u'Presupuesto base de licitación:')+pylatex.NoEscape('\dotfill') + pylatex.utils.bold(total_string))
        doc.append(pylatex.VerticalSpace('0.5cm'))
        doc.append(pylatex.NewLine())
        doc.append(u'Asciende el presente presupuesto base de licitación a la expresada cantidad de: ')
        doc.append(pylatex_utils.textsc(total_words))

