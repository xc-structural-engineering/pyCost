#PriceJustificationList.py

import pylatex
from pycost.prices.price_justification import PriceJustificationRecordContainer
from pycost.utils import basic_types
from decimal import Decimal

class PriceJustificationList(object):
    ''' Price justification list.

    :ivar cumulated_percentages: True if cumulated percentages
    :ivar mano_de_obra: labor (instance of PriceJustificationRecord class)
    :ivar materiales: materials (instance of PriceJustificationRecord class)
    :ivar maquinaria: machinery (instance of PriceJustificationRecord class)
    :ivar otros: not-classified elemental price (instance of PriceJustificationRecord class)
    :ivar percentages: percentage (ex: indirect costs) (instance of PriceJustificationRecord class)
    '''
    
    def __init__(self,pa, mano, mater, maqui, otr, perc):
        ''' Constructor.

        :param pa: True if cumulated percentages
        :param mano: labor (instance of PriceJustificationRecord class)
        :param mater: materials (instance of PriceJustificationRecord class)
        :param maqui: machinery (instance of PriceJustificationRecord class)
        :param otr: not-classified elemental price (instance of PriceJustificationRecord class)
        :param perc: percentage (ex: indirect costs) (instance of PriceJustificationRecordContainer class)
        '''
        self.cumulated_percentages= pa
        self.mano_de_obra= mano
        self.materiales= mater
        self.maquinaria= maqui
        self.otros= otr
        self.percentages= perc
        base= basic_types.ppl_price(self.Base())
        if self.cumulated_percentages:
            self.percentages.SetBaseAcum(base)
        else:
            self.percentages.SetBase(base)
    
    def Base(self):
        retval= basic_types.ppl_price(self.mano_de_obra.getTotal())
        retval+= self.materiales.getTotal()
        retval+= self.maquinaria.getTotal()
        retval+= self.otros.getTotal()
        return retval

    def getTotal(self):
        retval= basic_types.ppl_price(self.Base())
        retval+= self.percentages.getTotal()
        return retval

    def Redondeo(self):
        #return -self.getTotal().Redondeo()
        #XXX Redondeo para 2 decimales.
        tmp= self.getTotal()
        tmp*= Decimal('100')
        rnd= basic_types.ppl_price(round(tmp))-tmp
        rnd/= Decimal('100')
        return rnd

    def getRoundedTotal(self):
        return self.getTotal() + self.Redondeo()

    def getTotalCP1(self):
        return basic_types.ppl_price(float(self.getRoundedTotal()))

    def getLtxPriceString(self):
        ''' Return the price number in a human readable form.'''
        return basic_types.human_readable(self.getTotalCP1())

    def StrPriceToWords(self, genero):
        return basic_types.to_words(self.getTotalCP1(),genero)

    def __len__(self):
        return len(self.mano_de_obra)+len(self.materiales)+len(self.maquinaria)+len(self.otros)+len(self.percentages)


    def writePriceJustification(self, data_table):
        total= self.getTotal()
        rnd= self.Redondeo()
        total_rnd= self.getRoundedTotal()
        if(len(self)<2):
            row= [pylatex.table.MultiColumn(4, align='r',data=basic_types.sin_desc_string)]
            row.extend(['',''])
            data_table.add_row(row)
            #Total
            row= [pylatex.table.MultiColumn(4, align='r',data='Total')]
            row.append(pylatex.table.MultiColumn(2, align='r',data=pylatex.utils.bold(basic_types.human_readable(total))))
            data_table.add_row(row)
        else:
            self.mano_de_obra.writePriceJustification(data_table)
            self.materiales.writePriceJustification(data_table)
            self.maquinaria.writePriceJustification(data_table)
            self.otros.writePriceJustification(data_table)
            self.percentages.writePriceJustification(data_table)
            #Suma
            row= [pylatex.table.MultiColumn(4, align='r',data= pylatex.NoEscape("Suma\\ldots"))]
            row.append(pylatex.table.MultiColumn(2, align='r',data=pylatex.utils.bold(basic_types.human_readable(total))))
            data_table.add_row(row)
            
            #Redondeo
            row= [pylatex.table.MultiColumn(4, align='r',data= pylatex.NoEscape("Redondeo\\ldots"))]
            row.append(pylatex.table.MultiColumn(2, align='r',data=pylatex.utils.bold(basic_types.human_readable(rnd))))
            data_table.add_row(row)

            #Total
            row= [pylatex.table.MultiColumn(4, align='r',data= pylatex.NoEscape("Total\\ldots"))]
            row.append(pylatex.table.MultiColumn(2, align='r',data=pylatex.utils.bold(basic_types.human_readable(total_rnd))))
            data_table.add_row(row)

    def writePriceTableTwoIntoLatexDocument(self, data_table):
        total= self.getTotal()
        rnd= self.Redondeo()
        total_rnd= self.getRoundedTotal()
        if(len(self)<2):
            row1= ['','',basic_types.sin_desc_string,'']
            data_table.add_row(row1)
            row2= ['','',pylatex.utils.bold('TOTAL'),pylatex.utils.bold(basic_types.human_readable(total))]
            #Total
            data_table.add_row(row2)
        else:
            data_table.add_empty_row()
            self.mano_de_obra.writePriceTableTwoIntoLatexDocument(data_table)
            self.materiales.writePriceTableTwoIntoLatexDocument(data_table)
            self.maquinaria.writePriceTableTwoIntoLatexDocument(data_table)
            self.otros.writePriceTableTwoIntoLatexDocument(data_table)
            self.percentages.writePriceTableTwoIntoLatexDocumentPorc(data_table)
            #Suma
            row1= ['','',pylatex.NoEscape('Suma \ldots'),basic_types.human_readable(total)]
            data_table.add_row(row1)
            #Redondeo
            row2= ['','',pylatex.NoEscape('Redondeo \ldots'),basic_types.human_readable(rnd)]
            data_table.add_row(row2)
            #Total
            data_table.append(pylatex.Command(pylatex.NoEscape('cline{4-4}')))
            row3= ['','',pylatex.NoEscape('TOTAL\ldots'),basic_types.human_readable(total_rnd)]
            data_table.add_row(row3)


    def writePriceTableOneIntoLatexDocument(self, data_table, genero):
        data_table.add_row(['','','',self.StrPriceToWords(genero),self.getLtxPriceString()])


