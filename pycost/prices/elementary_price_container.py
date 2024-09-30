# -*- coding: utf-8 -*-
''' Elementary price container.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import pylatex
import logging
from pycost.prices import elementary_price
from pycost.utils import concept_dict
from pycost.utils import pylatex_utils
from pycost.utils import basic_types
from pycost.prices import component_list
from pycost.bc3 import codes

class ElementaryPrices(concept_dict.ConceptDict):
    ''' Container for elementary prices.'''
    
    def __init__(self):
        super(ElementaryPrices,self).__init__()

    def size(self, filterBy= None):
        ''' Return the number of elementary prices in this container. If 
        filterBy is not None return only the number of elementary prices 
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

    def newElementaryPrice(self, code, shortDescription, price, typ, unit, longDescription= None):
        ''' Define an elementary price.

        :param code: price identifier.
        :param shortDescription: short description of the price.
        :param typ: price type (labor, machinery, materials or unclassified).
        :param unit: unit (m, kg,...).
        :param longDescription: long description of the price.
        '''
        if(code in self.concepts):
            logging.warning('Code: '+code+' already exists in the price table.')
        newPrice= elementary_price.ElementaryPrice(cod=code, tit=shortDescription, ud= unit, p= price, tp= typ, long_description= longDescription)
        self.Append(newPrice)
        return newPrice
        
    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        if(conceptToRemoveCode in self.concepts):
            self.concepts.pop(conceptToRemoveCode)

    def writeSpreadsheet(self, sheet):
        logging.error("ElementaryPrices.writeSpreadsheet not implemented." + '\n')

    @staticmethod
    def writeLatexHeader(doc, tipo):
        ''' Write the header for the elementary prices table.

        :param doc: pylatex document to write into.
        :param tipo: type of the prices to write (maquinaria, materiales o mano de obra).
        '''
        str_tipo= basic_types.str_tipo(tipo)

        doc.append(pylatex.NoEscape(pylatex_utils.ltx_begin(textStr= "center") + '\n'))
        doc.append(pylatex_utils.LargeCommand())
        doc.append(" Precios elementales de " + str_tipo + ' ')
        doc.append(pylatex_utils.NormalSizeCommand())
        doc.append(pylatex.NoEscape(pylatex_utils.ltx_end("center") + '\n'))
        doc.append(pylatex_utils.SmallCommand())
        # Create LaTeX longtable.
        longTableStr= '|l|l|p{4cm}|r|'
        headerRow= [u'Código','Ud.',u'Denominación',u'Coste directo']
        with doc.create(pylatex_utils.LongTable(longTableStr)) as data_table:
            data_table.add_hline()
            data_table.add_row(headerRow)
            data_table.add_hline()
            data_table.end_table_header()
            data_table.add_hline()
            data_table.add_row((pylatex.table.MultiColumn(4, align='|r|',data='../..'),))
            data_table.add_hline()
            data_table.end_table_footer()
            data_table.add_hline()
            data_table.end_table_last_footer()
        return data_table

    def LeeMdoSpre(self, iS):
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
                precios= ''
                getline(iS,precios,'\n')
                pre= ''
                pos= precios.find('|')
                if pos<len(precios):
                    pre= precios.substr(0,pos)
                else:
                    pre= precios.substr(0,len(precios)-1)
                elem= elementary_price.ElementaryPrice(cod,tit,ud,atof(pre.c_str()),mdo)
                elem.texto_largo= tit
                self.Append(elem)
                if(iS.peek() == 26): break

        resto= ''
        getline(iS,resto,'\n')

    def LeeMaqSpre(self, iS):
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
                precios= ''
                getline(iS,precios,'\n')
                pre= ''
                pos= precios.find('|')
                if pos<1000:
                    pre= precios.substr(0,pos)
                else:
                    pre= precios.substr(0,len(precios)-1)
                elem= elementary_price.ElementaryPrice(cod,tit,ud,atof(pre.c_str()),maq)
                elem.texto_largo= tit
                self.Append(elem)
                if(iS.peek() == 26): break

        resto= ''
        getline(iS,resto,'\n')

    def LeeMatSpre(self, iS):
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
                precios= ''
                getline(iS,precios,'\n')
                pre= ''
                pos= precios.find('|')
                if pos<1000:
                    pre= precios.substr(0,pos)
                else:
                    pre= precios.substr(0,len(precios)-1)
                elem= elementary_price.ElementaryPrice(cod,tit,ud,atof(pre.c_str()),mat)
                elem.texto_largo= tit
                self.Append(elem)
                if(iS.peek() == 26): break

        resto= ''
        getline(iS,resto,'\n')


    def WriteSpre(self):
        ofs_mdo= std.ofstream("MDO001.std",std.ios.out)
        ofs_maq= std.ofstream("MAQ001.std",std.ios.out)
        ofs_mat= std.ofstream("MAT001.std",std.ios.out)
        for i in self:
            tipo= (i).second.getType()
            if(tipo==mdo):
                (i).second.WriteSpre(ofs_mdo)
                break
            elif(tipo==maq):
                (i).second.WriteSpre(ofs_maq)
                break
            elif(tipo==mat):
                (i).second.WriteSpre(ofs_mat)
                break
            else:
                (i).second.WriteSpre(ofs_mdo)
                break

        ofs_mdo.close()
        ofs_maq.close()
        ofs_mat.close()


    def LeeSpre(self, iS):
        Str= ''
        getline(iS,str,'\n')
        if(Str.find("[MDO]")<len(Str)): LeeMdoSpre(iS)
        getline(iS,Str,'\n')
        if(Str.find("[MAQ]")<len(Str)): LeeMaqSpre(iS)
        getline(iS,Str,'\n')
        if(Str.find("[MAT]")<len(Str)): LeeMatSpre(iS)

    def readBC3(self, els):
        ''' Read elementary prices from BC3 file.

        :param els: 
        '''
        if(els):
            sz= len(els)
            if(sz>0):
                logging.info("Reading elementary prices." + '\n')
                sz_inicial= len(self)
                keys= list(self.concepts.keys())
                for key in els.keys():
                    data= els.GetDatosElementaryPrice(key)
                    el= elementary_price.ElementaryPrice()
                    el.readBC3(data)
                    self.Append(el)

                num_agregados= len(self)-sz_inicial
                sz= len(els)
                if('SINDESCO' in els.keys()):
                    sz-= 1 # don't count SINDESCO
                if num_agregados != sz:
                    className= type(self).__name__
                    methodName= sys._getframe(0).f_code.co_name
                    logging.error(className+'.'+methodName+"; received: " + str(sz)
                              + " elementary prices but only "
                              + str(num_agregados)+ ' were loaded.\n')
                logging.info("Loaded " + str(sz) + " elementary prices. " + '\n')


    def writeLatexPricesOfType(self, doc, tipo, filterBy= None):
        ''' Write the header for the elementary prices table.

        :param doc: pylatex document to write into.
        :param tipo: type of the prices to write (maquinaria, materiales o mano de obra).
        :param filterBy: write those prices only.
        '''
        # Get concepts to write.
        filteredConcepts= list()
        for key in sorted(self.concepts):
            el= self.concepts[key]
            if(el.getType() == tipo):            
                if(filterBy is not None):
                    if(key in filterBy):
                        filteredConcepts.append(el)
                else:
                    filteredConcepts.append(el)
        
        if(len(filteredConcepts)>0):
            data_table= self.writeLatexHeader(doc, tipo)
            for el in filteredConcepts:
                el.writeLatex(data_table)
            doc.append(pylatex_utils.NormalSizeCommand())

    def writeLatex(self, doc, tipos= [basic_types.mdo, basic_types.maq, basic_types.mat], filterBy= None):
        ''' Write the header for the elementary prices table.

        :param doc: pylatex document to write into.
        :param tipos: types of the prices to write (maquinaria, materiales o mano de obra) defaults to all of them.
        :param filterBy: write those prices only.
        '''
        for tp in tipos:
            self.writeLatexPricesOfType(doc, tp, filterBy= filterBy)
            # doc.append(pylatex.NoEscape(pylatex_utils.ltx_newpage + '\n'))

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= super(ElementaryPrices, self).getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.

        :param dct: input dictionary.
        '''
        pendingLinks= list() # Links that cannot be set yet.
        if(dct):
            for key in dct:
                p= elementary_price.ElementaryPrice(key)
                itemDict= dct[key]
                pendingLinks.extend(p.setFromDict(itemDict))
                self.Append(p)
            pendingLinks.extend(super(ElementaryPrices, self).setFromDict(dct))
        return pendingLinks

    def clear(self):
        '''removes all items from the chapter.'''
        super(ElementaryPrices, self).clear()
