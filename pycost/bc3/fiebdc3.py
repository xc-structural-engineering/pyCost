# -*- coding: utf-8 -*-
'''Basic FIE BDC-3 utilities.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import logging
import re
import sys
from colorama import Fore
from colorama import Style

parameter_tokens_separator= '\t'

def es_codigo_obra(c):
    '''Returns true if c it's the code of a project.'''
    sz= len(c)
    if sz>1:
        return ((c[sz-2]=='#') and (c[sz-1]=='#'))
    else:
        return False

def es_codigo_capitulo(c):
    '''Returns true if c is a chapter code.'''
    retval= False
    sz= len(c)
    if es_codigo_capitulo_u_obra(c):
        if sz<2:
            retval= True; #Chapter without name.
        else:
            retval= (c[-2]!='#'); #Si no es obra, capítulo.
    return retval


def es_codigo_capitulo_u_obra(c):
    sz= len(c)
    if sz>0:
        return (c[-1]=='#')
    else:
        return False


def limpia_str(inputStr):
    retval= ''
    if(inputStr):
        retval= inputStr.replace(chr(10),'')
        retval= retval.replace(chr(13),'')
    return retval

def repl_lowcase_letter(match):
    '''In a group of type "([a-z]" replaces the 'a' by '0', 'b' by '1', ....'''
    match1=match.group(1)
    match1=ord(match1)-97
    return str(match1)

def repl_lowcase_letter_index(match):
    '''In a group of type "([a-z]," or ",[a-z])"  replaces the 'a' by '0', 'b' by '1', ....'''
    match1=match.group(1)
    match2 = match.group(2)
    match2=ord(match2)-97
    match3 = match.group(3)
    return match1+str(match2)+match3

def parse_comma_separated_list(inputString, delimiter= ',', quotationMark= '"'):
    retval= list()
    item= str()
    quotedString= False
    for c in inputString:
        if(c==quotationMark):
            item+= c
            if(not quotedString): # Quoted string starts.
                quotedString= True
            else: # Quoted string ends.
                quotedString= False
        else:
            if(c==delimiter and not quotedString): # item ends.
                retval.append(item)
                item= str()
            else:
                item+=c
    retval.append(item)
    return retval

class regBC3(object):
    def decod_bc3(self, strtk):
        logging.error('decod_bc3 not implemented.')
        return None

    def decod_str_bc3(self, Str):
        if(Str):
            if(len(Str)>0):
                self.decod_bc3(Str)
            
    def Write(self, os= sys.stdout):
        logging.error('Write not implemented.')


class regBC3_lista_reg(list, regBC3):
    def __init__(self, T, Str):
        ''' Constructor.
        
        :param T: object type.
        :param Str: string to decode.
        '''
        self.T= T
        if not (Str is None):
            self.decod_str_bc3(limpia_str(Str))
        
    def decod_bc3(self, strtk):
        ''' Decode the BC3 string argument.

        :param strtk: string to decode.
        '''
        if not strtk:
            return strtk # empty.
        else:
            for token in strtk:
                compData= token.split('\\')
                while(len(compData)>0):
                    code= compData.pop(0)
                    if(len(code)>0): # code not empty.
                        factor= 1.0
                        prodRate= 0.0
                        if(len(compData)>0):
                            tmp= compData.pop(0)
                            if(len(tmp)>0):
                                factor= float(tmp)
                        if(len(compData)>0):
                            tmp= compData.pop(0)
                            if(len(tmp)>0):
                                prodRate= float(tmp)
                        lt= self.T(Str= None)
                        lt.setValues(c= code, f= factor, pr= prodRate)
                        self.append(lt)
        return strtk
    
    def Write(self, os= sys.stdout):
        for i in self:
            i.Write(os)

class regBC3_lista_med(regBC3_lista_reg):
        
    def decod_bc3(self, strtk):
        ''' Decode the BC3 string argument.

        :param strtk: string to decode.
        '''
        if not strtk:
            return strtk # empty.
        else:
            lt= self.T(Str= None)
            lt.decod_bc3(strtk)
            self.append(lt)
        return strtk
    
    def Write(self, os= sys.stdout):
        for i in self:
            i.Write(os)



class regBC3_desc(regBC3):
    '''Element of a decomposition.

    :ivar codigo: Entity code
    :ivar factor: Entity factor
    :ivar productionRate: Entity output
    '''
    def __init__(self, Str):
        self.codigo= ''
        self.factor= 1.0 # factor defaults to 1.0
        self.productionRate= 0.0
        self.decod_str_bc3(limpia_str(Str))

    def setValues(self, c, f, pr):
        ''' Set the values of the object attributes.

        :param c: entity code.
        :param f: entity factor.
        :param pr: entity production rate.
        '''
        self.codigo= c
        self.factor= f
        self.productionRate= pr
        
    def decod_bc3(self, strtk):
        ''' decode tokens.'''
        tokens= strtk.split('\\')
        sz= len(tokens)
        if(sz>0): self.codigo= tokens[0]
        if(sz>1):
            token= tokens[1]
            if(len(token)>0): self.factor= float(token)
        if(sz>2):
            token= tokens[2]
            if(len(token)>0): self.productionRate= float(token)
        return strtk

    def isChapterOrObra(self):
        return (self.codigo.find("#")<self.codigo.leng.py())

    def isChapter(self):
        return es_codigo_capitulo(self.codigo)

    def EsObra(self):
        return es_codigo_obra(self.codigo)

    def Write(self, os= sys.stdout):
        os.write(u"Código: " + self.codigo + '\n'
           + "Factor: " + str(self.factor) + '\n'
           + "Production rate: " + str(self.productionRate) + '\n')


class regBC3_d(regBC3_lista_reg):
    ''' ~D type BC3 record.'''
    def __init__(self, Str):
        ''' Constructor.'''
        super(regBC3_d, self).__init__(T= regBC3_desc, Str= Str)

    def decod_bc3(self, strtk):
        '''La cadena que se pasa es la que queda a la derecha
           #de ~D|'''
        strtk_lista_desc= strtk.split('|')
        super(regBC3_d,self).decod_bc3(strtk= strtk_lista_desc)
        return strtk
    
    @staticmethod
    def isChapter(r, nombres_capitulo):
        '''Return true if the records is a chapter.'''
        retval= r.isChapter()
        if not retval:
            tmp= r.codigo+'#'
            retval= (tmp in nombres_capitulo)
        return retval

    def filterChapters(self, nombres_capitulo):
        '''Devuelve los elementos de la descomposición que son capítulos.'''
        retval= regBC3_d(Str= '')
        for i in self:
            if regBC3_d.isChapter(i,nombres_capitulo):
                retval.append(i)
        return retval
    
    def FiltraPrecios(self, nombres_capitulo):
        '''Devuelve los elementos de la descomposición que 
           son precios elementales o descompuestos.'''
        retval= regBC3_d(Str= '')
        for i in self:
            if not isChapter(i,nombres_capitulo):
                retval.append(i)
        return retval


class MedArq(regBC3):
    '''Mensuration lines.

    :ivar lines: mensuration lines
    '''
    def decod_bc3(self, strtk):
        '''String decodification.'''
        self.lines= list()
        tokens= strtk.split('\\')
        while(len(tokens)>0):
            tipo= 0
            comentario= ''
            unidades= 0
            largo= 0
            ancho= 0
            alto= 0
            if(len(tokens)>0):
                tmp= tokens.pop(0)
                if(len(tmp)>0):
                    tipo= int(tmp)
            if(len(tokens)>0):
                comentario= tokens.pop(0)
            if(len(tokens)>0):
                tmp= tokens.pop(0)
                if(len(tmp)>0):
                    unidades= float(tmp)
            if(len(tokens)>0):
                tmp= tokens.pop(0)
                if(len(tmp)>0):
                    largo= float(tmp)
            if(len(tokens)>0):
                tmp= tokens.pop(0)
                if(len(tmp)>0):
                    ancho= float(tmp)
            if(len(tokens)>0):
                tmp= tokens.pop(0)
                if(len(tmp)>0):
                    alto= float(tmp)
            # If any of the dimension is not null.
            if((unidades!= 0) or (largo!=0) or (ancho!=0) or (alto!=0)):
                if(unidades==0):
                    unidades= 1
                if(largo==0):
                    largo= 1
                if(ancho==0):
                    ancho= 1
                if(alto==0):
                    alto= 1
            lineData= {'tipo':tipo, 'comentario':comentario, 'unidades':unidades, 'largo':largo, 'ancho':ancho, 'alto':alto}
            self.lines.append(lineData)
        return strtk
    
    def Write(self, os= sys.stdout):
        for l in self.lines:
            os.write("Tipo: "+str(l['tipo'])+ '\n'
               + "Commentary: " + l['comentario'] + '\n'
               + "Units: " + str(l['unidades']) + '\n'
               + "Lenght: " + str(l['largo']) + '\n'
               + "Width: " + str(l['ancho']) + '\n'
               + "Height: " + str(l['alto']) + '\n')


class regBC3_linea_med(regBC3):
    '''Mensuration line.

    :ivar tipo: type
        0 (Vacio en el archivo)
        1 Subtotal parcial
        2 Subtotal acumulado.
        3 El comentario es una fórmula.
    :ivar med: (MedArq) mensuration
    '''
    def __init__(self, Str):
        self.med= MedArq()
        self.decod_str_bc3(limpia_str(Str))
        
    def decod_bc3(self, strtk):
        return self.med.decod_bc3(strtk)
    
    def Write(self,os):
        med.Write(os)


class regBC3_ruta(list, regBC3):
    def decod_bc3(self, strtk):
        '''Decodes string.'''
        self.extend(strtk.split('\\'))
        # Remove empty element at end.
        if(len(self[-1])==0):
            self.pop(-1)
        return strtk
        
    def Chapters(self):
        return len(self)-1

    def Posicion(self):
        return self[-1]

    def Write(self,os):
        Str= "Chapter: "
        for i in range(0,self.Chapters()):
            os.write(Str + self[i] + '\n')
            Str= "Sub" + Str
        os.write(u"Posición: " + self.Posicion())

class regBC3_m(regBC3):
    '''FIEBDC-3 ~M record

    :ivar ruta: path Cap/subcap/subsubcap/.../posicion
    :ivar med: (MedArq) mensuration
    '''
    def __init__(self, tokens):
        # Remove empty element at end.
        if(len(tokens[-1])==0):
            tokens.pop(-1)
        self.ruta= regBC3_ruta()
        if(len(tokens)>0):
            self.ruta.decod_bc3(tokens.pop(0))
        if(len(tokens)>0):
            self.med_total= float(tokens.pop(0))
        if(len(tokens)>0):
            self.decod_str_bc3(tokens)

    def decod_bc3(self, tokens):
        '''Decodes tokens.'''
        self.lista_med= MedArq()
        while (len(tokens)>0):
            tk= tokens.pop(0)
            self.lista_med.decod_bc3(tk)
        return tokens
    
    def Write(self, os= sys.stdout):
        os.write("Ruta: ")
        self.ruta.Write(os)
        os.write('\n' + "Total: " + str(self.med_total) + '\n')
        self.lista_med.Write(os)

class regBC3_c(regBC3):
    ''' FIEBDC ~C record.'''
    def __init__(self,Str):
        '''Constructor.

        :param Str: string to decode.
        '''
        self.unidad= ''
        self.resumen= ''
        self.precio= 0.0
        self.tipo= 0
        self.decod_str_bc3(Str)
        
    def getDict(self):
        ''' Return the member values in a dictionary.'''
        retval= dict()
        retval['unidad']= self.unidad
        retval['resumen']= self.resumen
        retval['precio']= self.precio
        retval['tipo']= self.tipo        
        return retval
    
    def setFromDict(self, dct):
        ''' Set the objects members from the values in the argument 
        dictionary.

        :param dct: input dictionary.
        '''
        self.unidad= dct['unidad']
        self.resumen= dct['resumen']
        self.precio= dct['precio']
        self.tipo= dct['tipo']
                
    def decod_bc3(self, tokens):
        '''Decodifies tokens.'''
        if(len(tokens)>0):
            self.unidad= tokens.pop(0)
        if(len(tokens)>0):        
            self.resumen= tokens.pop(0)
        if(len(tokens)>0):
            tmp= tokens.pop(0)
            if(len(tmp)>0):
                if(tmp.find('\\')):
                    tmp= tmp.split('\\')
                    tmp= tmp[0]
                self.precio= float(tmp)
        if(len(tokens)>0):
            self.fecha= tokens.pop(0)
        if(len(tokens)>0):
            tmp= tokens.pop(0)
            if(len(tmp)>0):
                if('%' in tmp):
                    self.tipo= tmp
                elif(tmp=='EA'): # See page 63 of the format definition
                    self.tipo= 0
                    self.subtype= 'Auxiliary element'
                else:
                    self.tipo= int(tmp)
        return tokens
    
    def Write(self, os= sys.stdout):
        os.write("Unidad: " + str(self.unidad) + '\n'
           + "Resumen: " + self.resumen + '\n'
           + "Precio: " + str(self.precio) + '\n'
           + "Fecha: " + self.fecha + '\n'
           + "Tipo: " + str(self.tipo) + '\n')

class regBC3_t(regBC3):
    '''Corresponds to a ~T record of BC3.'''
    def __init__(self,Str):
        self.texto= ''
        if(Str):
            self.decod_str_bc3(Str)
        
    def getDict(self):
        ''' Return the member values in a dictionary.'''
        retval= dict()
        retval['texto']= self.texto
        return retval
    
    def setFromDict(self, dct):
        ''' Set the objects members from the values in the argument 
        dictionary.

        :param dct: input dictionary.
        '''
        self.texto= dct['texto']
        
    def decod_bc3(self, tokens):
        '''Decodification.'''
        self.texto= tokens[0]
        return tokens
    
    def Write(self,os):
        os.write("Texto: " + self.texto + '\n')

class regBC3_p(regBC3):
    '''Corresponds to a ~P record of the FIEBDC-3 specification.'''
    def __init__(self,Str):
        self.variables= dict()
        self.components= dict()
        self.substitutionStatements= dict()
        self.parameterLabelStatements= dict()
        self.parameterLabelLetters= dict()
        if(Str):
            self.decod_str_bc3(Str)
            
    def getDict(self):
        ''' Return the member values in a dictionary.'''
        retval= dict()
        retval['variables']= self.variables
        retval['components']= self.components
        retval['substitutionStatements']= self.substitutionStatements
        retval['parameterLabelStatements']= self.parameterLabelStatements
        retval['parameterLabelLetters']= self.parameterLabelLetters
        return retval
    
    def setFromDict(self, dct):
        ''' Set the objects members from the values in the argument 
        dictionary.

        :param dct: input dictionary.
        '''
        self.variables= dct['variables']
        self.components= dct['components']
        self.substitutionStatements= dct['substitutionStatements']
        self.parameterLabelStatements= dct['parameterLabelStatements']
        self.parameterLabelLetters= dct['parameterLabelLetters']


    @staticmethod
    def isVariable(token):
        '''Return true if the token corresponds to a variable.

        :param token: text to analyze. 
        '''
        # See page 30 of the format definition document.
        retval= False
        prefix= token[0]
        if((prefix=='%') or (prefix=='$')):
            letter= token[1]
            if(letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N']):
                retval= True
            elif(letter in ['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']):
                retval= True
        return retval

    @staticmethod
    def isVariableAssignment(token):
        '''Return true if the token corresponds to a variable assignment.

        :param token: text to analyze. 
        '''
        retval= False
        if(self.isVariable(token)):
            if('=' in token):
                retval= True
        return retval
    
    @staticmethod
    def isDecompositionStatement(token):
        '''Return true if the token corresponds to decomposition statement.

        :param token: text to analyze.
        '''
        # See page 29 of the format definition document.
        retval= False
        if(':' in token):
            c= token.count(':')
            if(c<=2):
                expr= token.split(':')
                for v in expr[1:]:
                    if('$' in v):
                        return False
                retval= True
        return retval

    @staticmethod
    def isSubstitutionStatement(token):
        '''Return true if the token corresponds to a substitution statement.

        :param token: text to analyze. 
        '''
        substitutionStatements= ['RESUMEN', 'TEXTO', 'PLIEGO', 'CLAVES', 'COMERCIAL', 'R', 'T', 'P', 'K', 'F', 'SUMMARY', 'TEXT', 'SPECIFICATIONS', 'KEY', 'COmMERCIAL']
        # See page 29 of the format definition document.
        retval= False
        if('\\' in token):
            innerTokens= token.split('\\')
            firstLabel= innerTokens[1].strip()
            if(firstLabel in substitutionStatements):
                retval= True
        return retval
    
    @staticmethod
    def isParameterLabelStatement(token):
        '''Return true if the token corresponds to a parameter-label statement.

        :param token: text to analyze. 
        '''
        # See page 29 of the format definition document.
        retval= False
        if('\\' in token):
            if(not regBC3_p.isSubstitutionStatement(token)):
                retval= True
        return retval
    
    @staticmethod
    def isExpression(token):
        '''Return true if the token corresponds to an expression.

        :param token: text to analyze. 
        '''
        retval= False
        if('%' in token):
            retval= True
        if('/' in token):
            retval= True
        elif 'ATOF' in token:
            retval= True
        return retval

    def _decode_assignment_statement(self, itk):
        ''' Decode inner token corresponding to an assignment.

        :param itk: BC3 inner token.
        '''
        expr= itk.split('=', 1)
        leftHandSide= expr[0]
        if('(' in leftHandSide): # Has indexes.
            indexes= leftHandSide.split('(',1)[1].split(')')[0]
            if(',' in indexes):
                indexes= indexes.split(',')
            else:
                indexes= [indexes]
        else:
            indexes= []
        varName= leftHandSide[:2]
        prefix= itk[0]
        if(prefix=='%'): # Numerical assignment statement.
            if(self.isExpression(expr[1])): # is expression
                values= expr[1]
            else: # is list of values.
                values= expr[1].split(',')
                tmp= list()
                for v in values:
                    if(len(v)>0):
                        tmp.append(float(v))
                values= tmp
        elif(prefix=='$'):# Alphanumeric assignment statement.
            #values= re.split(r',(?=")', expr[1]) #expr[1].split(',')
            expr[1]= expr[1].replace('$', 'str')
            parsedValues= parse_comma_separated_list(expr[1])
            tmp= list()
            for parsedV in parsedValues:
                tmpStr= parsedV.strip()
                # Remove the double quotes only if it starts and ends with double quotes.
                if((tmpStr[0]=='"') and (tmpStr[-1]=='"')): # 
                   tmpStr= tmpStr[1:-1]
                tmp.append(tmpStr)
            if(len(tmp)>1):
                values= tmp
            elif(len(tmp)>0):
                values= tmp[0]
            else:
                logging.error('Something went wrong when parsing\''+itk+'\'')
                exit(1)
        varName= varName.replace('%', 'num')
        varName= varName.replace('$', 'str')
        if(len(indexes)>1): # is a matrix (not a vector)

            noRows= int(indexes[0])
            noCols= int(indexes[1])
            matrix= list()
            for i in range(0,noRows):
                row= list()
                for j in range(1,noCols+1):
                    ijElem= values.pop(0)
                    row.append(ijElem)
                matrix.append(row)
            values= matrix
        self.variables[varName]= values
        return varName, values

    def _decode_decomposition_statement(self, itk):
        ''' Decode inner token corresponding to a decomposition statement.

        :param itk: BC3 inner token corresponding to a decomposition statement.
        '''
        expr= itk.split(':')
        code= expr[0].strip()
        values= list()
        if code in self.components:
            values= self.components[code]
        values.append(expr[1].strip())
        if(len(expr)>2):
            values.append(expr[2].strip())
        return code, values
        
    def decod_bc3(self, tokens):
        '''Decodification.

        :param tokens: BC3 tokens to decode.
        '''
        for tk in tokens:
            innerTokens= tk.split(parameter_tokens_separator)
            substitutionStatementContinues= False
            for itk in innerTokens:
                itk= itk.strip()
                # remove comments.
                itk= itk.split('#', 1)[0]
                if(substitutionStatementContinues):
                    tmp= lastStatement
                    if(tmp[-1]!='.'):
                        tmp+= '.'
                    tmp+= ' '+itk
                    itk= tmp
                if(len(itk)>0):
                    if(self.isVariable(itk)):
                        if('=' in itk): # is asignment.
                           varName, values= self._decode_assignment_statement(itk)
                        else: #not assignment.
                            lastStatement= itk
                            substitutionStatementContinues= True
                    elif(self.isDecompositionStatement(itk)):
                        code, values= self._decode_decomposition_statement(itk)
                        self.components[code]= values
                    elif(self.isSubstitutionStatement(itk)):
                        lastChar= itk[-1]
                        if(lastChar in ['\\', '"', '+', '-', '*', '/']):
                            substitutionStatementContinues= False
                            expr= itk.split('\\')
                            if(itk[0]=='\\'):
                                key= expr[1].strip()
                                value= expr[2]
                            else:
                                key= expr[0]
                                value= expr[1]
                            self.substitutionStatements[key]= value
                        else:
                            lastStatement= itk
                            substitutionStatementContinues= True
                    elif(self.isParameterLabelStatement(itk)):
                        expr= itk.split('\\')
                        if(itk[0]=='\\'):
                            key= expr[1]
                            values= expr[2:]
                        else:
                            key= expr[0]
                            values= expr[1:]
                        key= key.strip()
                        key= key.replace(' ','_')
                        key= key.lower()
                        tmp= list()
                        for v in values:
                            if(len(v)>0):
                                v= v.strip()
                                v= v.replace(' >= ', '>=')
                                v= v.replace(' > ', '>')
                                v= v.replace(' <= ', '<=')
                                v= v.replace(' < ', '<')
                                tmp.append(v)
                        values= tmp
                        order= len(self.parameterLabelStatements)
                        if(order>3): # letter 'E' reserved for error (good design indeed).
                            order+= 1
                        letter= chr(order+ord('A'))
                        self.parameterLabelStatements[key]= values
                        self.parameterLabelLetters[key]= letter
                    else:
                        logging.error('Unknown token in parametric concept: \''+itk+'\'')
                        print(tokens)
                        exit(1)
        return tokens

    def writeParameterLabelStatements(self, os= sys.stdout):
        os.write(Fore.RED+"Parameter label statements:\n"+Style.RESET_ALL)
        for key in self.parameterLabelStatements:
            pl= self.parameterLabelStatements[key]
            keyString= Fore.GREEN+key+Style.RESET_ALL
            optionsString= Fore.YELLOW+str(pl)+Style.RESET_ALL
            os.write('  '+keyString+' : '+optionsString+'\n')
        
    
    def Write(self, os= sys.stdout):
        self.writeParameterLabelStatements(os)

class regBC3_elemento(object):
    ''' Elementary price according to FIEBDC-3 specification.

    :ivar concept: rebBC3_c object.
    :ivar txt: regBC3_t object.
    '''
    def __init__(self, c, t):
        ''' Constructor.

        :param c: concepto.
        :param t: texto.
        '''
        self.concept= c #Concepto.
        self.txt= t #Texto.

    def getDict(self):
        ''' Return the member values in a dictionary.'''
        retval= dict()
        retval['c']= self.concept.getDict()
        retval['t']= self.txt.getDict()
        return retval
    
    def setFromDict(self, dct):
        ''' Set the objects members from the values in the argument 
        dictionary.

        :param dct: input dictionary.
        '''
        concept= regBC3_c('')
        concept.setFromDict(dct['c'])
        self.concept= concept
        txt= regBC3_t('')
        txt.setFromDict(dct['t'])
        self.txt= txt
        
    def getTitle(self):
        return self.concept.resumen

    def Unidad(self):
        return self.concept.unidad

    def getPrice(self):
        return self.concept.precio

    def getType(self):
        return self.concept.tipo

    def Texto(self):
        return self.txt.texto

    def Write(self,os):
        self.concept.Write(os)
        self.txt.Write(os)

class regBC3_udobra(regBC3_elemento):
    def __init__(self,c,t,d):
        ''' Constructor.

        :param c: concept.
        :param t: text.
        :param d: components.
        '''        
        super(regBC3_udobra,self).__init__(c,t)
        self.desc= d # decomposition.
        
    def Write(self,os):
        super(regBC3_udobra,self).Write(os)
        self.desc.Write(os)
        
class regBC3_parametric(regBC3_elemento):
    ''' Parametric concept as defined in the FIEBDC-3 specification.

    :ivar parameters: regBC3_p object containing the parametric information.
    '''
    def __init__(self,c,t,p):
        ''' Constructor.

        :param c: concept.
        :param t: text.
        :param p: parameters.
        '''
        if(c is None):
            c= regBC3_c('')
        if(t is None):
            t= regBC3_t('')
        super(regBC3_parametric, self).__init__(c,t)
        if(p is None):
            p= regBC3_p('')
        self.parameters= p # parameters.

    def getParameterOptions(self, parameterKey:str):
        ''' Return the available options for the parameter
            identified by the key.

        :param parameterKey: identifier of the parameter.
        '''
        # get close parameter.
        retval= None
        if(parameterKey in self.parameters.parameterLabelStatements):
            retval= self.parameters.parameterLabelStatements[parameterKey]
        else:
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            logging.error(className+'.'+methodName+'; parameter: \''+parameterKey+'\' not found.')
        return retval
        
    def getDict(self):
        ''' Return the member values in a dictionary.'''
        retval= super().getDict()
        retval['parameters']= self.parameters.getDict()
        return retval

    def setFromDict(self, dct):
        ''' Set the objects members from the values in the argument 
        dictionary.

        :param dct: input dictionary.
        '''
        super().setFromDict(dct)
        self.parameters.setFromDict(dct['parameters'])

    def getParameterIndex(self, parameterKey:str, parameterOption:str):
        ''' Return the index of the parameterOption in the list of values
            corresponding to the parameter key.

        :param parameterKey: identifier of the parameter.
        :param parameterOption: identifier of the option chosen for the 
                                parameter.
        '''
        retval= None
        options= self.getParameterOptions(parameterKey)
        if(parameterOption in options):
            retval= options.index(parameterOption)
        else:
            logging.error('parameter: \''+parameterKey+'\' has not option: \''+parameterOption+'\'\n')
        return retval

    def computeSelectedParameters(self, options):
        ''' Return the indexes corresponding to the options argument.

        :param options: list of (parameterKey, parameterOption) tuples assigning
                       values to the parameters.
        '''
        selectedParameters= dict()
        for v in options:
            parameterKey= v[0] # identifier of the parameter.
            parameterOption= v[1] # option chose for this parameter.
            letter= self.parameters.parameterLabelLetters[parameterKey]
            index= self.getParameterIndex(parameterKey, parameterOption)
            # store selected parameters in dictionary
            numKey= 'num'+letter
            selectedParameters[numKey]= index
            strKey= 'str'+letter
            selectedParameters[strKey]= parameterOption
        return selectedParameters

    def getComponents(self, options):
        ''' Compute the components that correspond to the options argument.

        :param options: list of (parameterKey, parameterOption) tuples assigning
                       values to the parameters.
        '''
        retval= dict()
        selectedParameters= self.computeSelectedParameters(options)
        pattern= re.compile(r"\((\d+),(\d+)\)")
        for key in self.parameters.components:
            cList= self.parameters.components[key]
            for c in cList:
                c=re.sub(r'([a-z])',repl_lowcase_letter,c)
                c= c.replace('=', '==')
                c= c.replace('%', 'num')
                c= c.replace('$', 'str')
                c=c.replace('<>','!=')
                c=c.replace('@', ' or ')
                for i in range(0, len(selectedParameters)):
                    charToReplace= chr(ord('a')+i)
                    c= c.replace(charToReplace, str(i))
                for spKey in selectedParameters:
                    c= c.replace('('+spKey+')', '['+spKey+']')
                    value= selectedParameters[spKey]
                    c= c.replace(spKey, str(value))
                for varKey in self.parameters.variables:
                    value= self.parameters.variables[varKey]
                # Replace matrix indexes
                c= pattern.sub(r'[\1][\2]',c)
                c=c.replace('&','and')
                value= eval(c, self.parameters.variables)
                if(value!=0.0):
                    retval[key]= value
        return retval

    def getSubstitutionStatementValue(self, options, substitutionStatementNames):
        ''' Return the summary field.

        :param options: list of (parameterKey, parameterOption) tuples assigning
                       values to the parameters.
        :param substitutionStatementNames: names of the substitution statement
                                           (i. e.: ['RESUMEN, SUMMARY]).
        '''
        substitutionStatements= self.parameters.substitutionStatements
        retval= ''
        for name in substitutionStatementNames:
            if(name in substitutionStatements):
                retval= substitutionStatements[name]
                break
        retval= retval.replace('%', 'num')
        retval= retval.replace('$', 'str')
        retval= re.sub(r'(\()([a-z])(,)',repl_lowcase_letter_index,retval)
        retval= re.sub(r'(,)([a-z])(\))',repl_lowcase_letter_index,retval)
        retval= re.sub(r'str([A-Z])\(([a-zA-Z_0-9]*),([a-zA-Z_0-9]*)\)',r'str\1[\2][\3]',retval)
        # Replace selected values.
        selectedParameters= self.computeSelectedParameters(options)
        for spKey in selectedParameters:
            retval= retval.replace('('+spKey+')', '['+spKey+']')
            value= selectedParameters[spKey]
            retval= retval.replace(spKey, str(value))
        # Extract string replacement patterns (with brackets)
        p = re.compile(r"str[A-Z]\[[0-9]+\](?!\[)")
        replacements1= p.findall(retval)
        p = re.compile(r'str[A-Z]\[[a-zA-Z_0-9]*\]\[[a-zA-Z_0-9]*\]')
        replacements2=p.findall(retval)
        replacements=replacements1+replacements2
        for r in replacements:
            value= eval(r, self.parameters.variables)
            retval= retval.replace(r, value)
        # Extract number replacement patterns (with brackets)
        p = re.compile("(num[A-Z]\[[0-9]+\])")
        replacements= p.findall(retval)
        for r in replacements:
            value= eval(r, self.parameters.variables)
            retval= retval.replace(r, value)
        # Extract string replacement patterns (without brackets)
        p = re.compile(r'str[O-X]')
        replacements3= p.findall(retval)
        for r in replacements3:
            value= eval(r, self.parameters.variables)
            retval= retval.replace(r, value)
        # Extract number replacement patterns (without brackets)
        p = re.compile("(num[O-X]\[[0-9]+\])")
        replacements4= p.findall(retval)
        for r in replacements4:
            value= eval(r, self.parameters.variables)
            retval= retval.replace(r, value)
            
        return retval
    
    def getSummary(self, options):
        ''' Return the summary field.

        :param options: list of (parameterKey, parameterOption) tuples assigning
                        values to the parameters.
        '''
        return self.getSubstitutionStatementValue(options, ['RESUMEN', 'SUMMARY', 'R'])
    
    def getText(self, options):
        ''' Return the text field.

        :param options: list of (parameterKey, parameterOption) tuples assigning
                        values to the parameters.
        '''
        return self.getSubstitutionStatementValue(options, ['TEXTO', 'TEXT', 'T'])
    def getCodeTail(self, options):
        ''' Return the tail for the code of the instantiated concept.

        :param options: list of (parameterKey, parameterOption) tuples assigning
                        values to the parameters.
        '''
        retval= ''
        for v in options:
            parameterKey= v[0] # identifier of the parameter.
            parameterOption= v[1] # option chose for this parameter.
            letter= self.parameters.parameterLabelLetters[parameterKey]
            retval+= letter.lower()
        return retval

    def writeParameterOptions(self, os= sys.stdout):
        ''' Write the parameters and their options.'''
        self.parameters.writeParameterLabelStatements(os)

    def Write(self, os= sys.stdout):
        super(regBC3_parametric,self).Write(os)
        self.parameters.Write(os)

class regBC3_medicion(regBC3_elemento):
    def __init__(self,c,t,m):
        ''' Constructor.

        :param c: concepto.
        :param t: texto.
        :param m: measurements.
        '''        
        super(regBC3_medicion,self).__init__(c,t)
        self.med= m #Medicion.
        
    def Ruta(self):
        return self.med.ruta
    
    def Write(os):
        super(regBC3_medicion,self).Write(os)
        self.med.Write(os)

class regBC3_capitulo(regBC3_udobra):
    def __init__(self, c, t, d):
        ''' Constructor.

        :param c: concepto.
        :param t: texto.
        :param d: chapter components.
        '''        
        super(regBC3_capitulo,self).__init__(c,t,d)
        
    def filterChapters(self, nombres_capitulo):
        return self.desc.filterChapters(nombres_capitulo)

