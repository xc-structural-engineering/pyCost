# _*_ coding:utf-8 _*_
'''pylatex_utils.py: things that are not yet implemented in pylatex.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2017, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

from pathlib import Path
import os
import glob
import pylatex


class Part(pylatex.section.Section):
    '''A class that represents a part.'''

class Chapter(pylatex.section.Section):
    '''A class that represents a chapter.'''

class Paragraph(pylatex.section.Section):
    '''A class that represents a paragraph.'''

class Subparagraph(pylatex.section.Section):
    '''A class that represents a subparagraph.'''

class SmallCommand(pylatex.base_classes.CommandBase):
    '''
    small LaTeX command.
    '''

    _latex_name = 'small'

class NormalSizeCommand(pylatex.base_classes.CommandBase):
    '''
    small LaTeX command.
    '''

    _latex_name = 'normalsize'

class LargeCommand(pylatex.base_classes.CommandBase):
    '''
    Large LaTeX command.
    '''

    _latex_name = 'Large'

class largeCommand(pylatex.base_classes.CommandBase):
    '''
    large LaTeX command.
    '''

    _latex_name = 'large'


def textsc(s, escape=True):
    r"""Make a string appear textsc in LaTeX formatting.

    textsc() wraps a given string in the LaTeX command \textsc{}.

    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the textsc text will be escaped

    Returns
    -------
    NoEscape
        The formatted string.

    Examples
    --------
    >>> textsc("hello")
    '\\textsc{hello}'
    >>> print(textsc("hello"))
    \textsc{hello}
    """

    if escape:
        s = pylatex.escape_latex(s)

    return pylatex.NoEscape(r'\textsc{' + s + '}')


def input(s, escape=True):
    r"""Make LaTeX to read from a file.

    input() wraps a given string in the LaTeX command \input{}.

    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the input text will be escaped

    Returns
    -------
    NoEscape
        The formatted string.

    Examples
    --------
    >>> input("hello.tex")
    '\\input{hello.tex}'
    >>> print(input("hello.tex"))
    \input{hello.tex}
    """

    if escape:
        s = pylatex.escape_latex(s)

    return pylatex.NoEscape(r'\input{' + s + '}')

class LongTable(pylatex.table.LongTable):
    '''A class with the methods that are not yet implemented
       in the stable version of PyLatex.'''
    foot = False
    lastFoot = False

    def end_table_footer(self):
        r'''End the table foot which will appear on every page.'''

        if self.foot:
            msg = 'Table already has a foot'
            raise TableError(msg)

        self.foot = True

        self.append(pylatex.Command('endfoot'))

    def end_table_last_footer(self):
        r'''End the table foot which will appear on the last page.'''

        if self.lastFoot:
            msg = 'Table already has a last foot'
            raise TableError(msg)

        self.lastFoot = True

        self.append(pylatex.Command('endlastfoot'))

def getTabularDataFromList(listData):
    ''' Return tabular data in LaTeX format from the data stored in the
        list argument.

    :param listData: list of lists.
    '''
    retval= str()
    for row in listData:
        if(len(row)>0):
            retval+= row[0]
            for item in row[1:]:
                retval+= ' & ' + item
            retval+= '\\\\\n' # row ends.
            retval+= '\\hline\n' # hline
    return retval


def getLatexSection(parentSection):
    ''' Returns the section to use from this of its ancestor.'''
    if(parentSection == 'root'):
        return 'part'
    elif(parentSection == 'part'):
        return 'chapter'
    elif(parentSection == 'chapter'):
        return 'section'
    elif(parentSection == 'section'):
        return 'subsection'
    elif(parentSection == 'subsection'):
        return 'subsubsection'
    elif(parentSection == 'subsubsection'):
        return 'paragraph'
    elif(parentSection == 'paragraph'):
        return 'subparagraph'
    else:
        return None

def getPyLatexSection(sctName,title):
    if(sctName == 'part'):
        return Part(title)
    elif(sctName == 'chapter'):
        return Chapter(title)
    elif(sctName == 'section'):
        return pylatex.section.Section(title)
    elif(sctName == 'subsection'):
        return pylatex.section.Subsection(title)
    elif(sctName == 'subsubsection'):
        return pylatex.section.Subsubsection(title)
    elif(sctName == 'paragraph'):
        return Paragraph(title)
    elif(sctName == 'subparagraph'):
        return Subparagraph(title)
    else:
        return Subparagraph(title)
    

#ltx_percent= '\\%'
ltx_percent= '%'
ltx_ldots= '\\ldots'
def ltx_symbol(doc,s):
    doc.append('\\symbol{' + s + '}')

# Tipos de letra
ltx_tiny= '\\scriptsize'
ltx_scriptsize= '\\scriptsize'
ltx_large= '\\large'
def ltx_textbf(str):
    return '\\textbf{' + str + '}'
def ltx_emph(doc, str):
    return '\\emph{' + str + '}'

# Entornos
def ltx_begin(textStr):
    return '\\begin{' + textStr + '}'
def ltx_end(textStr):
    return '\\end{' + textStr + '}'

# Varios
ltx_newpage= '\\newpage'
def ltx_input(doc, textStr):
    doc.append('\\input{' + textStr + '}')

# Estructura

def ltx_part(doc,  textStr):
    doc.append('\\part{' + textStr + '}')
def ltx_star_part(doc,  textStr):
    doc.append('\\part*{' + textStr + '}')
def ltx_chapter(doc,  textStr):
    doc.append('\\chapter{' + textStr + '}')
def ltx_star_chapter(doc,  textStr):
    doc.append('\\chapter*{' + textStr + '}')
def ltx_section(doc,  textStr):
    doc.append('\\section{' + textStr + '}')
def ltx_subsection(doc,  textStr):
    doc.append('\\subsection{' + textStr + '}')
def ltx_subsubsection(doc,  textStr):
    doc.append('\\subsubsection{' + textStr + '}')
def ltx_paragraph(doc,  textStr):
    doc.append('\\paragraph{' + textStr + '}')

# Listas
ltx_beg_itemize= '\\begin{itemize}'
ltx_item= '\\item '
ltx_end_itemize= '\\end{itemize}'

# Tablas
ltx_ampsnd= ' & '
ltx_fin_reg= ' \\\\'
ltx_hline= '\\hline'
ltx_endhead= '\\endhead'
ltx_endfoot= '\\endfoot'
ltx_endlastfoot= '\\endlastfoot'
def ltx_cline(doc,  textStr):
    doc.append('\\cline{' + textStr + '}')
def ltx_datos_multicolumn( num_campos, just, texto):
    return ('{' + num_campos + '}{' + just + '}{' + texto + '}')
def ltx_multicolumn(textStr):
    return '\\multicolumn' + textStr

def ascii2latex(s):
    '''Return the equivalent latex code.'''
    tmp= s
    # if type(s) == textStr:
    #     # Ignore errors even if the string is not proper UTF-8 or has
    #     # broken marker bytes.
    #     # Python built-in function unicode() can do this.
    #     tmp= unicode(s, encoding= 'utf-8', errors='ignore')
    # else:
    #     # Assume the value object has proper __unicode__() method
    #     tmp= unicode(s)
    #tmp= s.encode('ascii',errors='replace') #unicode(s, errors='replace')
    if(tmp.find('\\')): # Has scape characters.
     tmp.replace('\\(','(')
    if(tmp.find('\\')):
     tmp.replace('\\)',')')
    if(tmp.find('\\')):
     tmp.replace('\\[','[')
    if(tmp.find('\\')):
     tmp.replace('\\]',']')
    retval= ''
    for c in tmp:
        if(c=='_'): retval+= '\\'
        if(c=='%'): retval+= '\\'
        if(c=='$'): retval+= '\\'
        if(c=='&'): retval+= '\\'
        if(c=='>'):
            retval+= '$>$'
            continue
        retval+= c
    return retval

def removeLtxTemporaryFiles(latexFileName):
    ''' Remove LaTeX temporary files corresponding to the file name argument.

    :param latexFileName: name of the latex file.
    '''
    fileName= Path(latexFileName).stem # Get file name without extension.
    temporaryFilesExtensions= ['aux', 'bmt', 'lof', 'log', 'lot', 'ptc*', 'mtc*', 'toc', 'idx', 'maf', 'out'] # regular LaTeX temporary files.
    temporaryFilesExtensions.extend(['4ct', '4tc', 'css', 'idv', 'lg', 'tmp', 'xref']) # htlatex temporary files.
    for ext in temporaryFilesExtensions:
        searchFor= fileName+'.'+ext
        fileList= glob.glob(searchFor)
        for filePath in fileList:
            try:
                os.remove(filePath)
            except:
                logging.error("Error while deleting file : ", filePath)        
