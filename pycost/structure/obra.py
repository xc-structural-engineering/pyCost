# -*- coding: utf-8 -*-
''' Root chapter.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys
import yaml
import json
import xmltodict
from dicttoxml import dicttoxml
import xml.dom.minidom
import pickle
import logging
import pylatex
from pycost.structure import chapter as cp
from pycost.structure import unit_price_quantities
from pycost.utils import percentages as pc
from pycost.bc3 import codigos_obra as cod
from pycost.prices import elementary_price
from pycost.prices import unit_price
from pycost.utils import pylatex_utils
from pycost.utils import basic_types
from pycost.bc3 import fiebdc3
import tempfile
import re # strip comments
from openpyxl import Workbook


def preprocess_file(inputFile):
    ''' Put each BC3 record in one line.

    :param inputFile: input file.
    '''
    separator= '~'
    def stripComments(code):
        code = str(code)
        return re.sub(r'(?m)#.*\n', '\n', code)
    def each_chunk(stream):
        buffer = ''
        while True:  # until EOF
            chunk = stream.read(4096)
            if not chunk:  # EOF?
                yield buffer
                break
            buffer+= chunk
            while True:  # until no separator is found
                try:
                    part, buffer = buffer.split(separator, 1)
                except ValueError:
                    break
                else:
                    yield part
    def replace_newlines_inside_string(inputString):
        ''' Replace \n characters between double quotation marks (").

        :param inputString: input string.
        '''
        retval= ''
        insideDoubleQuotation= False
        for c in inputString:
            if(c=='"'):
                insideDoubleQuotation= not insideDoubleQuotation
            if(c=='\n') and insideDoubleQuotation:
                c= ' '#'std::endl' # for later processing.
            retval+= c
        return retval
    tmpFile= tempfile.NamedTemporaryFile(suffix='.bc3', mode='w', encoding='utf-8', delete=False)
    for chunk in each_chunk(inputFile):
        if(len(chunk)>0):
            if(chunk[0]=='P'): # Parametric concept.
                chunk= stripComments(chunk) # Remove comments.
                chunk= replace_newlines_inside_string(chunk)
                chunk= re.sub('\n\n+', '\n', chunk) # Remove multiple \n
                chunk= re.sub('\s+\n', '\n', chunk) # Remove spaces
                chunk= re.sub('\n\s+', '\n', chunk)
                chunk= chunk.replace('\t',' ')
                chunk= chunk.replace('=\n','= ')
                chunk= chunk.replace('+\n','+ ')
                chunk= chunk.replace(',\n',', ')
                chunk= chunk.replace('.\n','. ')
                chunk= chunk.replace('\n',fiebdc3.parameter_tokens_separator) # replace newline characters.
            else:    
                chunk= chunk.replace('\n','') # remove newline characters.
            chunk= separator+chunk+'\n'
            tmpFile.write(chunk)  # writing chunk by chunk.
    tmpFile.close()
    return tmpFile.name

class Obra(cp.Chapter):
    ''' Construction site class.

    :ivar percentages: percentage tables.
    '''
    def __init__(self, cod="ObraSinCod", tit="ObraSinTit"):
        ''' Constructor.

        :param cod: construction site codename.
        :param tit: constuction site description.
        '''
        super(Obra,self).__init__(cod,tit,1,1)
        elem= elementary_price.ElementaryPrice("SINDESCO",basic_types.sin_desc_string,"",1.0,basic_types.mat)
        self.precios.Elementales().Append(elem)
        self.percentages= pc.Percentages()

    def isRootChapter(self):
        ''' Returns true.'''
        return True
    
    def getHeight(self):
        ''' Return the height of the tree.'''
        self.setOwner(parent= self) # Compute chapters owners.
        return super(Obra,self).getHeight()
    
    def nombre_clase(self):
        return "Obra"

    def WriteSpre(self):
        precios.WriteSpre()
        logging.error(u"Exportación de capítulos no implementada." + '\n')

    def getUnitPrice(self, cod):
        ''' Tries to return the unit price identified by the code argument.
            Issues an error if failed.

        :param cod: unit price identifier.
        '''
        retval= super(Obra,self).findPrice(cod)
        if not retval:
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            logging.error(className+'.'+methodName+'; unit price: '+ cod + ' not found.')
            exit(1)
        return retval
    
    def replacePrices(self, replacementsTable):
        ''' Replace the prices as indicated by the pairs 
            [oldPriceCode, newPriceCode] in the argument table.

        :param replacementsTable: list of replacement pairs.
        '''
        # De-reference the new prices.
        newReplacementsTable= list()
        for pair in replacementsTable:
            oldPriceCode= pair[0]
            newPriceCode= pair[1]
            newPrice= self.getUnitPrice(newPriceCode)
            if(newPrice):
                newReplacementsTable.append([oldPriceCode, newPrice])
        # Call the ancestor method with de-referenced new prices.
        super(Obra, self).replacePrices(newReplacementsTable)
        
    def CodigoBC3(self):
        return super(Obra,self).CodigoBC3() + "#"

    def newChapter(self, cap_padre, cap):
        ''' Appends the chapter to the sub-chapter
            obtained from the string of the form 1\2\1\4.

        :param cap_padre: identifier of the parent chapter.
        :param cap: chapter to add.
        '''
        if(cap_padre==""): #root chapter.
            subcapitulos.newChapter(cap)
        else:
            self.BuscaSubcapitulo(cap_padre).newSubChapter(cap)

    def appendUnitPriceQuantities(self, cap_padre, m):
        ''' Appends la partida being passed as parameter
            to the sub-chapter indicated by the string
            of the form 1\2\1\4.'''
        BuscaSubcapitulo(cap_padre).appendUnitPriceQuantities(m)

    def LeeMedicSpre(self, inputFile):
        cdg= ""
        while(not inputFile.eof()):
            if self.peek(inputFile,1)==26:
                resto= ''
                getline(inputFile,resto,'\n')
                continue

            lista= ''
            getline(inputFile,lista,'|')
            if(lista==""): break
            if(lista!=cdg): #capitulo nuevo
                cod= replace(lista,'/','_')
                tit= ''
                getline(inputFile,tit,'\n')
                tit= q_blancos(tit.substr(0,len(tit)-1))
                logging.error(u"Cargando capítulo: " + cod + ' ' + tit + '*' + '\n')
                cp= Chapter(cod,tit)
                ruta= replace(lista,'/','\\')
                pos= ruta.find('\\')
                if(pos>len(ruta)): #Es capítulo raiz.
                    newChapter("",cp)
                else: #es capitulo.pyijo.
                    pos2= ruta.rfind('\\')
                    ruta= ruta.substr(0,pos2)
                    newChapter(ruta,cp)

                cdg= lista
            else: #Medicion
                cod= replace(lista,'/','\\')
                contenido= ''
                getline(inputFile,contenido,'\n')
                pos= contenido.find('|')
                cod_ud_obra= contenido.substr(0,pos)
                contenido= contenido.substr(pos+1,len(contenido))
                udo= precios.searchForUnitPrice(cod_ud_obra)
                if not udo:
                    logging.error("Unidad de obra: " + cod_ud_obra
                              + " no encontrada" + '\n')
                    return

                muo= UnitPriceQuantities(udo)
                while(True):
                    pos= contenido.find('|')
                    comentario= contenido.substr(0,pos)
                    contenido= contenido.substr(pos+1,len(contenido))
                    pos= contenido.find('|')
                    uds= contenido.substr(0,pos)
                    contenido= contenido.substr(pos+1,len(contenido))
                    pos= contenido.find('|')
                    lng= contenido.substr(0,pos)
                    contenido= contenido.substr(pos+1,len(contenido))
                    pos= contenido.find('|')
                    lat= contenido.substr(0,pos)
                    contenido= contenido.substr(pos+1,len(contenido))

                    pos= contenido.find('|')
                    alt= ""
                    if pos>len(contenido):
                        pos= contenido.find('\n')
                        alt= contenido.substr(0,pos-1)
                        rm= MeasurementRecord(comentario,float(uds),float(lng),float(lat),float(alt))
                        muo.Append(rm)
                        break

                    else:
                        alt= contenido.substr(0,pos)
                        contenido= contenido.substr(pos+1,len(contenido))
                        rm= MeasurementRecord(comentario,float(uds),float(lng),float(lat),float(alt))
                        muo.Append(rm)


                appendUnitPriceQuantities(cod,muo)

    def LeeSpre(self, inputFile):
        Str= ''
        precios.LeeSpre(inputFile)
        getline(inputFile,Str,'\n')
        if Str.find("[MED]")<len(Str):
            LeeMedicSpre(inputFile)


    def findChapterMedicion(self,ruta):
        ruta.pop(-1) #Eliminamos el último elemento que es la posición.
        return self.BuscaSubcapitulo(ruta)


    def LeeBC3DatosObra(self, rootChapterDict):
        if(len(rootChapterDict)<1):
            className= type(self).__name__
            methodName= sys._getframe(0).f_code.co_name
            logging.error(className+'.'+methodName+'; root chapter not found.')
        key= next(iter(rootChapterDict)) # first key
        rootChapter= rootChapterDict[key]
        reg= rootChapterDict.getChapterData(key= key)
        self.codigo= reg.Codigo(); # code
        self.title= reg.Datos().getTitle(); # title
        components= reg.Datos().desc
        self.subcapitulos.newChapters(components)

    def readQuantitiesFromBC3(self, co):
        ''' Read measurements records from a FIEBDC-3 file.

        :param co: measurement records.
        '''
        retval= True
        med= co.getQuantityData()
        if(len(med)<1):
            logging.info("No quantities in BC3 file.")
        for i in med:
            reg= med.GetDatosMedicion(i)
            # UnitPrice *ud= precios.searchForUnitPrice(reg.CodigoUnidad())
            tmp= reg.CodigoUnidad()
            cod_unidad= reg.CodigoUnidad().partition('@')[0]
            ud= self.findPrice(cod_unidad)
            if not ud:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; no se encontró el precio: \'" + cod_unidad + "\'" + '\n')
                logging.error(u"  El concepto de código: \'" + cod_unidad + "\'")
                if not co.ExisteConcepto(cod_unidad):
                    logging.error(" no existe." + '\n')
                else:
                    logging.error(" exists in the table: "
                              + co.StrTablaConcepto(cod_unidad) + '\n')
                retval= False
            else:
                m= unit_price_quantities.UnitPriceQuantities(ud)
                m.readBC3(reg.Datos())
                ruta= reg.Datos().Ruta()
                chapterCode= reg.getChapterCode()
                c= self.findChapterMedicion(ruta)
                if not c:
                    c= self.BuscaCodigo(chapterCode)
                if c:
                    c.appendUnitPriceQuantities(m)
                else:
                    className= type(self).__name__
                    methodName= sys._getframe(0).f_code.co_name
                    c= self.findPrice(chapterCode)
                    if(c):
                        logging.error(className+'.'+methodName+"; parent concept '"+str(chapterCode)+ "' is not a chapter. Measurements outside chapters are not supported yet.\n")
                        retval= False
                    else:
                        className= type(self).__name__
                        methodName= sys._getframe(0).f_code.co_name
                        logging.error(className+'.'+methodName+"; chapter with code '"+str(chapterCode)+ "' not found.\n")
                        retval= False
        return retval

    def readBC3(self, inputFile):
        ''' Read data from FIEBDC 3 file.

        :param inputFile: input file to read from.
        '''
        tmpFileName= preprocess_file(inputFile)
        tmpFile= open(tmpFileName, 'r')
        co= cod.CodigosObra()
        logging.info("Reading FIEBDC 3 records...")
        co.readBC3(tmpFile) #Reads BC3 records.
        logging.info("done." + '\n')
        logging.info(u"Leyendo estructura de capítulos...")
        self.LeeBC3DatosObra(co.GetDatosObra())
        self.subcapitulos.LeeBC3Caps(co); #Lee capitulos y precios elementales.
        logging.info("done." + '\n')

        logging.info("Reading prices...")
        self.precios.LeeBC3Elementales(co.GetDatosElementos()); #Lee los precios elementales fuera de capítulo.

        #LeeBC3DescFase1(co); #Lee descompuestos de capitulos.
        unitCosts= co.GetDatosUnidades()
        self.precios.LeeBC3DescompFase1(unitCosts)

        logging.info("done." + '\n')
        logging.info("Leyendo descomposiciones...")

        #pendientes= LeeBC3DescFase2(co); #Lee descomposiciones.
        pendientes= self.precios.LeeBC3DescompFase2(unitCosts, rootChapter= self)

        logging.info("done." + '\n')
        # logging.info("Leyendo precios globales...")
        # self.precios.LeeBC3DescompFase1(co.GetDatosUnidades())
        # tmp= self.precios.LeeBC3DescompFase2(co.GetDatosUnidades())
        # logging.info("num. precios= " + str(self.precios.NumDescompuestos()) + '\n')
        # pendientes.update(tmp)
        logging.info("done." + '\n')
        if(len(pendientes)>0):
            logging.info("   Leyendo descomposiciones (y 2)...")
            #pendientes= LeeBC3DescFase2(co); #Lee descomposiciones.
            pendientes= precios.LeeBC3DescompFase2(co.GetDatosUnidades(), rootChapter= self); #Lee descomposiciones.
            logging.info("done." + '\n')
            logging.info("   Leyendo precios globales (y 2)...")
            precios.LeeBC3DescompFase1(co.GetDatosUnidades())
            tmp= precios.LeeBC3DescompFase2(co.GetDatosUnidades(), rootChapter= self)
            pendientes.insert(tmp.begin(),tmp.end())
            logging.info("done." + '\n')

        logging.info("Reading quantities...")

        retval= self.readQuantitiesFromBC3(co)
        logging.info("done." + '\n')
        return retval

    def ImprLtxPresEjecMat(self, doc, signaturesFileName= 'firmas'):
        ''' Write the budget for material execution.

        :param doc: pylatex document to write into.
        :param signaturesFileName: name of the file containing the signatures.
        '''
        headerText= u'Presupuesto de ejecución material'
        chapter= pylatex_utils.Chapter(title= headerText,numbering= False)
        chapter.append(pylatex.Command('cleardoublepage'))
        center= pylatex.Center()
        center.append(pylatex_utils.LargeCommand())
        center.append(pylatex.utils.bold(headerText))
        center.append(pylatex_utils.largeCommand())
        chapter.append(center)
        chapter.append(pylatex.VerticalSpace('2cm'))
        self.subcapitulos.ImprLtxResumen(chapter,"",False)
        chapter.append(pylatex.utils.bold(headerText))
        chapter.append(pylatex.Command('dotfill'))
        ltxPriceString= self.getLtxPriceString()
        chapter.append(pylatex.utils.bold(ltxPriceString))
        chapter.append(pylatex.VerticalSpace('0.5cm'))
        chapter.append(pylatex.NewLine())
        chapter.append(u'Asciende el presente presupuesto de ejecución material a la expresada cantidad de: ')
        roundedPrice= self.getRoundedPrice()
        chapter.append(pylatex_utils.textsc(basic_types.to_words(roundedPrice,False)))
        if(signaturesFileName):
            chapter.append(pylatex.Command('input{'+signaturesFileName+'}'))
        doc.append(chapter)

    def getFinalPrices(self, symbol):
        ''' Return a dictionary containing the final prices.
        '''
        roundedPrice= self.getRoundedPrice()
        return self.percentages.getFinalPrices(roundedPrice, symbol= symbol)
        
    def ImprLtxPresContrata(self, doc, signaturesFileName= 'firmas'):
        ''' Write the contract execution budget.

        :param doc: pylatex document to write into.
        :param signaturesFileName: name of the file containing the signatures.
        '''
        headerText= u'Presupuesto base de licitación'
        chapter= pylatex_utils.Chapter(title= headerText,numbering= False)
        chapter.append(pylatex.Command('cleardoublepage'))
        center= pylatex.Center()
        center.append(pylatex_utils.LargeCommand())
        center.append(pylatex.utils.bold(headerText))
        center.append(pylatex_utils.largeCommand())
        chapter.append(center)
        chapter.append(pylatex.VerticalSpace('2cm'))
        roundedPrice= self.getRoundedPrice()
        self.percentages.printLtx(chapter, roundedPrice)
        if(signaturesFileName):
            chapter.append(pylatex.Command('input{'+signaturesFileName+'}'))
        doc.append(chapter)

    def WriteBC3(self, os, pos= ''):
        os.write("~V|XC, S.L.|FIEBDC-3/2012|pyCost 0.1|\n")
        self.WritePreciosBC3(os)
        self.WriteConceptoBC3(os)
        self.WriteDescompBC3(os)
        self.WriteQuantitiesBC3(os,pos)
        self.WriteSubChaptersBC3(os,pos)

    def ImprLtxPresGen(self, doc):
        ''' Write the general budget.

        :param doc: pylatex document to write into.
        '''
        part= pylatex_utils.Part("Presupuestos Generales")
        self.ImprLtxPresEjecMat(part)
        self.ImprLtxPresContrata(part)
        doc.append(part)

    def writeQuantitiesIntoLatexDocument(self, doc, superTabular= False):
        ''' Write measurements report.

        :param doc: pylatex document to write into.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        super(Obra,self).writeQuantitiesIntoLatexDocument(doc,'root', superTabular= superTabular)

    def ImprCompLtxMed(self, doc, other):
        ''' Write measurements comparison report.

        :param doc: pylatex document to write into.
        :param other: project to compare with.
        '''
        doc.create(pylatex_utils.ltx_part(basic_types.quantitiesCaption) + '\n')
        doc.create(pylatex.Command('parttoc'))
        doc.create(pylatex_utils.ltx_begin("landscape") + '\n')
        super(Obra,self).ImprCompLtxMed(os,'root',other)
        doc.create(pylatex_utils.ltx_end("landscape") + '\n')

    def writePriceTableOneIntoLatexDocument(self, doc, signaturesFileName= 'firmas', filterBy= None, superTabular= False):
        '''
        :param signaturesFileName: name of the file containing the signatures.
        :param filterBy: write those prices only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        part= pylatex_utils.Part("Cuadro de precios no. 1")
        part.append(pylatex.Command('parttoc'))
        part.append(pylatex.Command('setcounter{chapter}{0}'))
        super(Obra,self).writePriceTableOneIntoLatexDocument(part,'root', filterBy= filterBy, superTabular= superTabular)
        if(signaturesFileName):
            part.append(pylatex.Command('input{'+signaturesFileName+'}'))
        doc.append(part)

    def writePriceTableTwoIntoLatexDocument(self, doc, signaturesFileName= 'firmas', filterBy= None, superTabular= False):
        '''Write price table two.

        :param doc: pylatex document to write into.
        :param signaturesFileName: name of the file containing the signatures.
        :param filterBy: write the prices on the list only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        part= pylatex_utils.Part("Cuadro de precios no. 2")
        part.append(pylatex.Command('parttoc'))
        part.append(pylatex.Command('setcounter{chapter}{0}'))
        super(Obra,self).writePriceTableTwoIntoLatexDocument(part,'root', filterBy= filterBy, superTabular= superTabular)
        if(signaturesFileName):
            part.append(pylatex.Command('input{'+signaturesFileName+'}'))
        doc.append(part)

    def writeElementaryPrices(self, doc, tipos=  [basic_types.mdo, basic_types.maq, basic_types.mat], filterBy= None, superTabular= False, sctName= 'part'):
        ''' Write the elementary prices table.

        :param doc: pylatex document to write into.
        :param tipos: types of the prices to write (maquinaria, materiales o mano de obra) defaults to all of them.
        :param filterBy: write the prices on the list only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        :param sctName: type of section (from 'part' until 'subparagraph'), if
                        None, don't create a section for the elementary prices.
        '''
        if(sctName is None):
            outputDoc= doc
        else:
            outputDoc= pylatex_utils.getPyLatexSection(sctName= sctName, title= "Precios elementales")
        super(Obra,self).writeElementaryPrices(doc= outputDoc, parentSection= 'root', tipos= tipos, filterBy= filterBy, superTabular= superTabular)
        if(sctName):
            doc.append(outputDoc)
            
    def writePriceJustification(self, doc, signaturesFileName= 'firmas', filterBy= None, superTabular= False, sctName= 'part'):
        ''' Write price justification.

        :param doc: pylatex document to write into.
        :param signaturesFileName: name of the file containing the signatures.
        :param filterBy: write price justification for those prices only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        :param sctName: type of section (from 'part' until 'subparagraph'), if
                        None, don't create a section for the elementary prices.
        :returns: list of the written prices.
        '''
        if(sctName is None):
            outputDoc= doc
        else:
            outputDoc= pylatex_utils.getPyLatexSection(sctName= sctName, title= "Justificación de precios")
            
        retval= super(Obra,self).writePriceJustification(outputDoc, 'root', filterBy= filterBy, superTabular= superTabular)
        if(signaturesFileName):
            outputDoc.append(pylatex.Command('input{'+signaturesFileName+'}'))
        if(sctName):
            doc.append(outputDoc)
        if(filterBy is not None):
            missingPrices= list() # prices that are in filterBy but have not been printed.
            for p in filterBy:
                if not p in retval:
                    missingPrices.append(p)
            if(len(missingPrices)>0):
                logging.warning('The following prices are missing: '+str(missingPrices))
        return retval

    def writePriceTablesIntoLatexDocument(self, doc, filterBy= None, superTabular= False):
        ''' Write price tables 1 and 2.

        :param doc: pylatex document to write into.
        :param filterBy: write price tables for those prices only.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        self.writePriceTableOneIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular)
        self.writePriceTableTwoIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular)

    def writePartialBudgetsIntoLatexDocument(self, doc, superTabular= False):
        ''' Write partial budgets report.

        :param doc: pylatex document to write into.
        :param superTabular: if true use a supertabular LaTeX environment,
                             otherwise use longtable.
        '''
        super(Obra,self).writePartialBudgetsIntoLatexDocument(doc,'root', superTabular= superTabular)

    def ImprCompLtxPreParc(self, doc, other):
        ''' Compare partial budgets and write a report.

        :param doc: pylatex document to write into.
        :param other: project to compare with.
        '''
        part= pylatex_utils.Part('Presupuestos parciales')
        part.append(pylatex.Command('parttoc'))
        part.append(pylatex.Command('setcounter{chapter}{0}'))
        part.append(pylatex_utils.ltx_begin("landscape") + '\n')
        super(Obra,self).ImprCompLtxPre(part,'root',other)
        part.append(pylatex_utils.ltx_end("landscape") + '\n')
        doc.append(part)

    def ImprLtxResumen(self, doc):
        ''' Write partial budgets summary.

        :param doc: pylatex document to write into.
        '''
        part= pylatex_utils.Part('Resumen de los presupuestos parciales')
        chapter= pylatex_utils.Chapter(title= 'Resumen',numbering= False)
        part.append(chapter)
        super(Obra,self).ImprLtxResumen(chapter, parentSection= 'root')
        doc.append(part)

    def ImprCompLtx(self, doc, other, superTabular= False):
        ''' Prints the comparison with another project.

        :param doc: pylatex document to write into.
        :param other: project to compare with.
        '''
        #ImprCompLtxMed(other,os)
        self.ImprCompLtxMed(doc,other)
        precios.writePriceTablesIntoLatexDocument(os, superTabular= superTabular); #Price tables.
        self.ImprCompLtxPreParc(doc,other)
        #ImprLtxResumen(os)

    def writeIntoLatexDocument(self, doc, filterBy= None, superTabular= False):
        ''' Write budget in the pylatex document argument.

        :param doc: pylatex document to write into.
        :param filterBy: write those prices only.
        '''
        self.writeQuantitiesIntoLatexDocument(doc, superTabular= superTabular) #Quantities.
        self.writePriceTablesIntoLatexDocument(doc, filterBy= filterBy, superTabular= superTabular) #Price lists.
        self.writePartialBudgetsIntoLatexDocument(doc, superTabular= superTabular) #Presupuestos parciales.
        self.ImprLtxResumen(doc) #Resument presup. parciales.
        self.ImprLtxPresGen(doc) #Presupuestos generales.
        return doc
    
    def getLatexDocument(self):
        '''get the construction budget in LaTeX format.'''
        retval= pylatex.Document(documentclass= 'book')
        retval.packages.append(pylatex.Package('minitoc'))
        retval.append(pylatex.Command('doparttoc'))
        self.writeIntoLatexDocument(retval)
        return retval

    def getPriceReportLatexDocument(self, superTabular= False):
        '''Prints the report in latex format.

        :param superTabular: if true, use supertabular instead of longtable.
        '''
        retval= pylatex.Document(documentclass= 'article')
        if(superTabular):
            retval.packages.append(pylatex.Package('supertabular'))
        quantitiesReport= self.getQuantitiesReport()
        quantitiesReport.printLtx(retval, superTabular= superTabular)
        return retval
    
    def writeSpreadsheetSummary(self, sheet, maxDepth):
        ''' Write partial budgets summary.

        :param book: spreadsheet book.
        '''
        self.setOwner(parent= self) # Compute chapters owners.
        sheet.append(['Resumen de los presupuestos parciales'])
        super(Obra,self).writeSpreadsheetSummary(sheet, depth= 0, maxDepth= maxDepth)

    def writeSpreadsheetQuantities(self,sheet):
        ''' Write the quantities in the work book argument.

        :param book: spreadsheet book.
        '''
        sheet.append([self.getTitle()])
        super(Obra, self).writeSpreadsheetQuantities(sheet, parentSection= 'root')
        
    def writeSpreadsheetBudget(self, sheet):
        sheet.append([self.getTitle()])
        super(Obra, self).writeSpreadsheetBudget(sheet, parentSection= 'root')
        
    def writeSpreadsheet(self, outputFileName, summaryMaxDepth= None):
        ''' Write data using spreadsheet format
 
        :param outputFile: name of the output file.
        '''
        # Create spreadsheet book and sheets
        wbook = Workbook()
        quantSheet=wbook.create_sheet("Mediciones")
        priz1Sheet=wbook.create_sheet("CuaPre1")
        priz2Sheet=wbook.create_sheet("CuaPre2")
        partbdgSheet=wbook.create_sheet("PreParc")
        summSheet=wbook.create_sheet("Resumen")
        elemprizSheet=wbook.create_sheet("Elementales")
        pyexcel.save_book_as(bookdict=sheetNames, dest_file_name= outputFileName)
        book= pyexcel.get_book(file_name=outputFileName)
        # Populate it with quantities.
        self.writeSpreadsheetQuantities(quantSheet)
        # with prices.
        self.precios.writeSpreadsheet(partbdgSheet)
        # and with partial budgets.
        self.writeSpreadsheetBudget(partbdgSheet)
        # write summary.
        if(not summaryMaxDepth):
            summaryMaxDepth= self.getHeight()
        self.writeSpreadsheetSummary(summSheet, maxDepth= summaryMaxDepth)
        # Save the modified document.
        book.save_as(outputFileName)

    def getPriceDescriptions(self, codes, latex= True):
        ''' Return a list populated with the codes and the corresponding
            descriptions.

        :param codes: list of the codes of the desired descriptions.
        '''
        retval= list()
        for code in codes:
            txtCode= code
            unitPrice= self.findPrice(code)
            if(unitPrice):
                unit= unitPrice.unidad
                description= unitPrice.long_description
                if(latex):
                    txtCode= pylatex_utils.ascii2latex(txtCode)
                    unit= pylatex_utils.ascii2latex(unit)
                    description= pylatex_utils.ascii2latex(description)
                retval.append([txtCode, unit, description])
            else:
                className= type(self).__name__
                methodName= sys._getframe(0).f_code.co_name
                logging.error(className+'.'+methodName+"; no se encontró el precio: \'" + code + "\'\n")
                
        return retval

    def SimulaDescomp(self, origen, destino):
        precios.SimulaDescomp(origen,destino)

    def solvePendingLinks(self, pendingLinks):
        ''' Solve object pending links.

        :param pendingLinks: list of pending links.
        '''
        super().solvePendingLinks(pendingLinks= pendingLinks)
        self.setOwner(parent= self) # Compute chapters ownership.
        return pendingLinks
        
    def readFromYaml(self, inputFileName):
        ''' Load data from a YAML file.

        :param inputFileName: name of the input file.
        '''
        # Read data from file.
        inputFile= open(inputFileName, mode='r')
        dataDict= yaml.safe_load(inputFile)
        inputFile.close()
        pendingLinks= self.solvePendingLinks(self.setFromDict(dataDict))
        return pendingLinks
    
    def writeYaml(self, outputFileName):
        ''' Write data to a YAML file.

        :param outputFileName: name of the output file.
        '''
        # Read data from file.
        outputFile= open(outputFileName, mode='w')
        outputs= yaml.dump(self.getDict(), outputFile, allow_unicode=True)
        outputFile.close()
        
    def readFromXml(self, inputFileName):
        ''' Load data from a XML file.

        :param inputFileName: name of the input file.
        '''
        # Read data from file.
        inputFile= open(inputFileName, mode='r')
        xmlString= inputFile.read()
        inputFile.close()
        dataDict= xmltodict.parse(xmlString)
        pendingLinks= self.solvePendingLinks(self.setFromDict(dataDict['pyCost']))
        return pendingLinks
    
    def writeXml(self, outputFileName, indent= 2):
        ''' Write data to a XML file.

        :param outputFileName: name of the output file.
        '''
        # Read data from file.
        xml_string = dicttoxml(self.getDict(), custom_root='pyCost', attr_type=False)
        dom = xml.dom.minidom.parseString(xml_string)
        pretty_xml_as_string = dom.toprettyxml()
        outputFile= open(outputFileName, mode='w')
        outputFile.write(pretty_xml_as_string)
        outputFile.close()

    def readFromDictionaries(self, elementaryPricesDict, unitPricesDict):
        ''' Read prices from data stored in dictionaries. The field names in
            the dictionaries must correspond to those used in 
            getDict/setFromDict methods.

        :param elementaryPricesDict: dictionary storing the elementary prices data.
        :param unitPricesDict: dictionary storing the unit prices data.
        '''
        # Append elementary prices.
        for key in elementaryPricesDict:
            fields= elementaryPricesDict[key]
            tmp= elementary_price.ElementaryPrice(cod= fields['code'])
            tmp.setFromDict(fields)
            self.precios.elementos.Append(tmp)

        pendingLinks= list() # Links that cannot be set yet.
        # Append unit prices.
        for key in unitPricesDict:
            fields= unitPricesDict[key]
            tmp= unit_price.UnitPrice(cod= fields['code'])
            pendingLinks.extend(tmp.setFromDict(fields))
            self.precios.unidades.Append(tmp)

        return self.solvePendingLinks(pendingLinks)


        
        
def bc3_to_yaml(inputFileName, outputFileName, cod='CodelessRoot', tit= 'TitlelessRoot'):
    ''' Reads a BC3 file and creates the corresponding YAML format file.

    :param inputFileName: name of the input file.
    :param cod: construction site codename.
    :param tit: constuction site description.
    '''
    # Create root object.
    site= Obra(cod= cod, tit= tit)

    # Read data from file.
    inputFile= open(inputFileName,mode='r', encoding="latin-1")

    site.readBC3(inputFile)
    inputFile.close()

    # Write in YAML format
    with open(outputFileName, 'w') as outputFile:
        outputs= yaml.dump(site.getDict(), outputFile, allow_unicode=True)
    outputFile.close()

def yaml_to_pickle(inputFileName, outputFileName, cod='CodelessRoot', tit= 'TitlelessRoot'):
    ''' Reads a YAML file and creates the corresponding pickle format file.

    :param inputFileName: name of the input file.
    :param cod: construction site codename.
    :param tit: constuction site description.
    '''
    # Create root object.
    site= Obra(cod= cod, tit= tit)

    # Read data from file.
    pendingLinks= site.readFromYaml(inputFileName)
    # Dump into pickle file.
    with open(outputFileName, 'wb') as fh:
        pickle.dump(site, fh)

def pickle_to_yaml(inputFileName, outputFileName):
    ''' Reads a pickle file and creates the corresponding YAML format file.

    :param inputFileName: name of the input file.
    :param cod: construction site codename.
    :param tit: constuction site description.
    '''
    # Read root object.
    inputFile= open(inputFileName, 'rb')
    rootChapter= pickle.load(inputFile)
    inputFile.close()

    # Write into YAML file.
    rootChapter.writeYaml(outputFileName)
    
def pickle_to_json(inputFileName, outputFileName):
    ''' Reads a pickle file and creates the corresponding YAML format file.

    :param inputFileName: name of the input file.
    :param cod: construction site codename.
    :param tit: constuction site description.
    '''
    # Read root object.
    inputFile= open(inputFileName, 'rb')
    rootChapter= pickle.load(inputFile)
    inputFile.close()

    # Write into JSON file.
    rootChapter.writeJson(outputFileName)

def yaml_to_json(inputFileName, outputFileName, cod='CodelessRoot', tit= 'TitlelessRoot'):
    ''' Reads a YAML file and creates the corresponding json format file.

    :param inputFileName: name of the input file.
    :param cod: construction site codename.
    :param tit: constuction site description.
    '''
    # Create root object.
    rootChapter= Obra(cod= cod, tit= tit)

    # Read data from file.
    pendingLinks= rootChapter.readFromYaml(inputFileName)

    # Write into JSON file.
    rootChapter.writeJson(outputFileName)


