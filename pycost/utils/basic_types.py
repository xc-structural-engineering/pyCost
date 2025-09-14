# -*- coding: utf-8 -*-
'''Basic data types.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from decimal import getcontext, Decimal
from num2words import num2words
import locale

localeString= 'es_ES.utf-8'
l= locale.setlocale(locale.LC_ALL, localeString)

''' TIPO: Tipo de concepto, se reservan los siguientes tipos: '''

''' 0 (Sin clasificar) 1 (Mano de obra), 2 (Maquinaria y medios aux.), 3 (Materiales). '''

sin_clasif, mdo, maq, mat= range(0, 4)

def str2tipo_concepto(Str):
    if(len(Str)<1):
        return sin_clasif
    elif(Str[0]=='0'):
        return sin_clasif
    elif(Str[0]=='1'):
        return mdo
    elif(Str[0]=='2'):
        return maq
    elif(Str[0]=='3'):
        return mat
    else:
        return sin_clasif

def sint2tipo_concepto(si):
    if(si==0):
        return sin_clasif
    elif(si==1):
        return mdo
    elif(si==2):
        return maq
    elif(si==3):
        return mat
    else:
        return sin_clasif

def tipo_concepto2str(t):
    if(t==0):
        return "sin_clasif"
    elif(t==1):
        return "mdo"
    elif(t==2):
        return "maq"
    elif(t==3):
        return "mat"
    else:
        return "sin_clasif"
    return "sin_clasif"

def tipo_concepto2chr(tp):
    if(tp==sin_clasif):
        return '0'
    elif(tp==mdo):
        return '1'
    elif(tp==maq):
        return '2'
    elif(tp==mat):
        return '3'
    else:
        return '0'

pricePrecision= 2
pricePlaces= Decimal(10) ** -pricePrecision
priceFormatString= '{0:.'+str(pricePrecision)+'f}'

def ppl_price(price):
    txtPrice= priceFormatString.format(price)
    return Decimal(txtPrice)

justificationPrecision= 3
justificationPlaces= Decimal(10) ** -justificationPrecision
justificationFormatString= '{0:.'+str(justificationPrecision)+'f}'

def ppl_justification(perc):
    txtJustification=  justificationFormatString.format(perc)
    return Decimal(txtJustification)
    
percentagePrecision= 3
percentagePlaces= Decimal(10) ** -percentagePrecision
percentageFormatString= '{0:.'+str(percentagePrecision)+'f}'

def ppl_percentage(perc):
    txtPercentage=  percentageFormatString.format(perc)
    return Decimal(txtPercentage)

def str_tipo(tipo):
    retval= ''
    if(tipo==mdo):
        retval= 'mano de obra'
    elif(tipo==maq):
        retval= 'maquinaria'
    elif(tipo==mat):
        retval= 'materiales'
    else:
        retval= 'sin clasificar'
    return retval

quantitiesCaption= 'Mediciones'
partialBudgetsCaption= 'Presupuestos parciales'

sin_desc_string= u'sin_desc'

def to_words(number, genre, lng= 'es'):
    return num2words(number, lang= lng, to='currency')

def human_readable(number, decPlaces= 3):
    ''' Return a string containing the number in a human readable form.

    :param number: number to convert.
    :param decPlaces: number of decimal places.
    '''
    #return locale.format('%d',number, grouping= True)
    formatString= '%10.'+str(decPlaces)+'f'
    return locale.format_string(formatString, number, grouping= True)

def human_readable_currency(number, symbol= False, grouping=True):
    ''' Return a string containing the number in a human readable form.

    :param number: number to convert.
    :param symbol: if true add currency symbol to the string.
    :param grouping: 
    '''
    return locale.currency(number, symbol= symbol, grouping= grouping)

