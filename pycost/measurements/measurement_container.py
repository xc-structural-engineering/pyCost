# -*- coding: utf-8 -*-
'''ChapterQuantities.py quantities inside a chapter.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import pylatex
from pycost.structure import unit_price_quantities
from pycost.measurements import measurement_report
from pycost.measurements import measurement_record
#import Pieza
from pycost.utils import EntPyCost as epc

from pycost.utils import pylatex_utils
from pycost.utils import basic_types

class ChapterQuantities(list, epc.EntPyCost):
    ''' Quantities inside a chapter. '''
    
    def __init__(self):
        super(ChapterQuantities, self).__init__()
        epc.EntPyCost.__init__(self, owner= None)

    def appendToExistingCode(self, unitPriceQuantities):
        ''' Tries to append the argument to an existing code on
        this container. In it doesn't exists it creates a new
        record.
        
        :param unitPriceQuantities: quantities to append.
        '''
        unitPriceCode= unitPriceQuantities.getUnitPriceCode()
        codeFound= False
        for upq in self: # search for the code in this container.
            uPCode= upq.getUnitPriceCode()
            if(uPCode==unitPriceCode): # code found.
                upq.quantities.extend(unitPriceQuantities.quantities)
                codeFound= True
        if(not codeFound):
            super(ChapterQuantities, self).append(unitPriceQuantities)

    def getQuantitiesForPrice(self, unitPriceCode):
        ''' Return the quantities corresponding to the price with the
            given code.

        :param unitPriceCode: code of the price whose quantities will be
                              retrieved.
        '''
        retval= None
        codeFound= False
        for upq in self: # search for the code in this container.
            uPCode= upq.getUnitPriceCode()
            if(uPCode == unitPriceCode): # code found.
                retval= upq
                break
        return retval
 
    def removeConcept(self, conceptToRemoveCode):
        ''' Remove the concept whose code is being passed as parameter.

        :param conceptToRemoveCode: code of the concept to remove.
        '''
        itemsToRemove= self.getConceptsThatDependOn(conceptToRemoveCode)
        for item in itemsToRemove:
            self.remove(item)

    def getConceptsThatDependOn(self, priceCode):
        ''' Return the prices measurements which depend on the one whose code
            is passed as parameter.

        :param priceCode: code of the price on which the returned prices depend.
        '''
        retval= list()
        for upq in self: # search for the code in this container.
            uPCode= upq.getUnitPriceCode()
            if(uPCode==priceCode): # code found.
                retval.append(upCode)
        return retval
           
    def getLtxPriceString(self):
        ''' Return the price in as a string in human readable format.'''
        return basic_types.human_readable_currency(self.getRoundedPrice())

    def getPrice(self):
        t= 0.0
        for i in self:
            t+=(i).getPrice()
        return t

    def getRoundedPrice(self):
        t= basic_types.ppl_price(0.0)
        for item in self:
            t+= item.getRoundedPrice()
        return t

    def Write(self, os, cod, pos):
        contador= 1
        for i in self:
            pos_med= pos + str(contador) + '\\'
            (i).WriteBC3(os,cod,pos_med)
            contador+= 1

    def WriteDescompBC3(self, os, cod):
        if(len(self)<1):
            return
        else:
            os.write("~D" + '|' #Antes estaba con ~Y (daba problemas)
             + cod + '|')
            for i in self:
                os.write((i).getUnitPriceCode() + "\\1\\" #factor 1
                   + str((i).getRoundedTotal()) + '\\')
            os.write('|' + '\n')

    def ImprCompLtxMed(self, doc, other):
        ''' Write a LaTeX report containing a comparison of the measurements.

        :param doc: pylatex documents to write into.
        :param other: project to compare with.
        '''
        if len(self):
            doc.append(pylatex_utils.ltx_tiny + '\n')
            doc.append(pylatex_utils.ltx_begin("longtable}{lrrrrr|lrrrrr") + '\n'
               + "\\multicolumn{6}{c|}{\\normalsize\\textbf{Proyecto de construcción}\\tiny} &"
               + "\\multicolumn{6}{c}{\\normalsize\\textbf{Proyecto modificado}\\tiny} \\\\"
               + '\n' + pylatex_utils.ltx_hline + '\n'
               + pylatex_utils.ltx_endhead + '\n'
               + "\\multicolumn{12}{r}{../..}\\\\" + '\n'
               + pylatex_utils.ltx_endfoot + '\n'
               + pylatex_utils.ltx_endlastfoot + '\n')
            for i in self:
                 cod= (i).getUnitPriceCode()
                 for j in other:
                    if(cod == (j).getUnitPriceCode()): break
                    if(j!=other.end()): #Found it!
                        (i).ImprCompLtxMed(os,*(j))
                    else:
                        (i).ImprCompLtxMed(os)
            doc.append("\\end{longtable}" + '\n')
            doc.append(pylatex_utils.NormalSizeCommand())

    def writeQuantitiesIntoLatexDocument(self, doc, superTabular= False):
        ''' Write quantities into pylatex document.

        :param doc: pylatex document to write into.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
       '''
        if len(self):
            num_fields= 6
            longTableStr= 'lrrrrr'
            if(superTabular):
                # Create LaTeX supertabular.
                ## Remove/redefine previous heads and tails.
                pylatex_utils.supertabular_first_head(doc, firstHeadStr= '')
                pylatex_utils.supertabular_head(doc, headStr= '')
                superTabularTailStr= '\\multicolumn{'+str(num_fields)+'}{r}{../..}\\\\%\n'
                pylatex_utils.supertabular_tail(doc, tailStr= superTabularTailStr)
                pylatex_utils.supertabular_last_tail(doc, lastTailStr= '')
                with doc.create(pylatex_utils.SuperTabular(longTableStr)) as data_table:
                    pass
            else:
                # Create LaTeX longtable.
                with doc.create(pylatex_utils.LongTable(longTableStr)) as data_table:
                    data_table.add_row((pylatex.table.MultiColumn(num_fields, align='r',data='../..'),))
                    data_table.end_table_footer()
                    data_table.end_table_last_footer()
            for i in self:
                (i).writeQuantitiesIntoLatexDocument(data_table, superTabular= superTabular)
            doc.append(pylatex.Command('newpage'))

    def ImprCompLtxPre(self, doc, tit, other, tit_other):
        ''' Write comparison report.

        :param doc: pylatex document to write into.
        :param tit: project title.
        :param other: project to compare with.
        :param tit_other: title of the other project.
        '''
        if size():
            doc.append(pylatex_utils.ltx_tiny + '\n')
            doc.append(pylatex_utils.ltx_begin("longtable}{lrlrr|lrlrr") + '\n'
               + "\\multicolumn{5}{c|}{\\normalsize\\textbf{Proyecto de construcción}\\tiny} &"
               + "\\multicolumn{5}{c}{\\normalsize\\textbf{Proyecto modificado}\\tiny} \\\\"
               + '\n' + pylatex_utils.ltx_hline + '\n'
               + "Partida & Cantidad & Descripción & \\multicolumn{1}{p{1.5cm}}{P. unitario} & Importe & Partida & Cantidad & Descripción & \\multicolumn{1}{p{1.5cm}}{P. unitario} & Importe \\\\" + '\n'
               + pylatex_utils.ltx_hline + '\n'
               + pylatex_utils.ltx_endhead + '\n'
               + "\\multicolumn{10}{r}{../..}\\\\" + '\n'
               + pylatex_utils.ltx_endfoot + '\n'
               + pylatex_utils.ltx_endlastfoot + '\n')
            for i in self:
                 cod= (i).getUnitPriceCode()
                 for j in other:
                     if(cod == (j).getUnitPriceCode()): break
                 if(j!=other.end()): #Found it!
                     (i).ImprCompLtxPre(os,*(j))
                 else:
                     (i).ImprCompLtxPre(os)

            doc.append("\\multicolumn{4}{p{8cm}}{\\textbf{Total: "
               + tit_other + "}} & \\textbf{" + other.getLtxPriceString() + "} & " + '\n')
            doc.append("\\multicolumn{4}{p{8cm}}{\\textbf{Total: "
               + tit + "}} & \\textbf{" + getLtxPriceString() + "}\\\\" + '\n')
            doc.append("\\end{longtable}" + '\n')
            doc.append(pylatex_utils.NormalSizeCommand())

    def writePartialBudgetsIntoLatexDocument(self, doc, tit, superTabular= False):
        ''' Write partial budgets into pylatex document.

        :param doc: pylatex document to write into.
        :param tit: title of the corresponding chapter.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        if len(self):
            doc.append(pylatex_utils.SmallCommand())
            num_fields= 5
            longTableStr= 'lrlrr'
            if(superTabular):
                # Create LaTeX supertabular.
                ## Remove/redefine previous heads and tails.
                header_row= ['Partida','Cantidad',u'Descripción']
                header_row.append('\\multicolumn{1}{p{1.5cm}}{Precio unitario}')
                header_row.append('Importe')                
                superTabularHeaderStr= '&'.join(header_row)+'\\\\%\n\\hline%\n'
                pylatex_utils.supertabular_first_head(doc, firstHeadStr= superTabularHeaderStr)
                pylatex_utils.supertabular_head(doc, headStr= superTabularHeaderStr)
                superTabularTailStr= '\\multicolumn{'+str(num_fields)+'}{r}{../..}\\\\%\n'
                pylatex_utils.supertabular_tail(doc, tailStr= superTabularTailStr)
                pylatex_utils.supertabular_last_tail(doc, lastTailStr= '\\hline%\n')
                with doc.create(pylatex_utils.SuperTabular(longTableStr)) as data_table:
                    pass
            else:                                            
                # Create LaTeX longtable.
                header_row= ['Partida','Cantidad',u'Descripción']
                header_row.append(pylatex.table.MultiColumn(1, align=pylatex.utils.NoEscape('p{1.5cm}'),data='Precio unitario'))
                header_row.append('Importe')
                with doc.create(pylatex_utils.LongTable(longTableStr)) as data_table:
                    data_table.add_row(header_row)
                    data_table.add_hline()
                    data_table.end_table_header()
                    data_table.add_row((pylatex.table.MultiColumn(num_fields, align='r',data='../..'),))
                    data_table.end_table_footer()
                    data_table.add_hline()
                    data_table.end_table_last_footer()
            for i in self:
                (i).writePartialBudgetsIntoLatexDocument(data_table)
            data_table.add_row([pylatex.table.MultiColumn(4, align=pylatex.utils.NoEscape('p{8cm}'),data=pylatex.utils.bold('Total: '+tit)),pylatex.utils.bold(self.getLtxPriceString())])
            doc.append(pylatex_utils.NormalSizeCommand())


    def writeSpreadsheetQuantities(self, sheet):
        ''' Write the quantities in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        '''
        for i in self:
            (i).writeSpreadsheetQuantities(sheet)

    def writeSpreadsheetBudget(self, sheet):
        ''' Write the budgets in the spreadsheet argument.

        :param sheet: spreadsheet to write into.
        '''
        for i in self:
            (i).writeSpreadsheetBudget(sheet)

    def getQuantitiesReport(self):
        ''' Return a report containing the total measurement for 
            each unit price.'''
        retval= measurement_report.QuantitiesReport()
        for i in self:
            retval.Inserta((i).Report())
        return retval

    def getDict(self):
        ''' Return a dictionary containing the object data.'''
        retval= epc.EntPyCost.getDict(self)
        for idx, i in enumerate(self):
            retval[idx]= i.getDict()
        return retval
        
    def setFromDict(self,dct):
        ''' Read member values from a dictionary.'''
        pendingLinks= list()
        if(dct):
            for key in dct:
                itemDict= dct[key]
                item= unit_price_quantities.UnitPriceQuantities()
                pendingLinks.extend(item.setFromDict(itemDict))
                self.append(item)
        return pendingLinks
    
    def clear(self):
        '''removes all items from the chapter.'''
        for sc in self:
            sc.clear()
        super(ChapterQuantities, self).clear()
