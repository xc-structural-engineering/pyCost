# -*- coding: utf-8 -*-
''' Concept tree related utilities.'''

__author__= "Luis C. Pérez Tato (LCPT)"
__copyright__= "Copyright 2025, LCPT"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@ciccp.es"

import sys

def print_tree(current_node, indent="", last='updown', includeTitles= False, os= sys.stdout):
    ''' Print the tree structure from the current node to the leaves 
        hanging from it.
    '''

    nb_subcapitulos = lambda node: sum(nb_subcapitulos(child) for child in node.subcapitulos) + 1
    size_branch = {child: nb_subcapitulos(child) for child in current_node.subcapitulos}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.subcapitulos, key=lambda node: nb_subcapitulos(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    current_node_text= current_node.Codigo()
    if(includeTitles):
        current_node_text+= ' '+current_node.title
    """ Printing of "up" branch. """
    for child in up:     
        next_last = 'up' if up.index(child) == 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node_text))
        print_tree(child, indent=next_indent, last=next_last, includeTitles= includeTitles, os= os)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    os.write('{0}{1}{2}{3}'.format(indent, start_shape, current_node_text, end_shape)+'\n')

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node_text))
        print_tree(child, indent=next_indent, last=next_last, includeTitles= includeTitles, os= os)

