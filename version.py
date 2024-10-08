# -*- coding: utf-8 -*-
''' Manage the package version.'''

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2024, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com" "ana.ortega.ort@gmail.com"

import json
import os
import subprocess

__version__ = "0.5.0"

jsonFileName= "last_pycost_version.json"

def get_git_revision_short_hash() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('ascii').strip()

if os.path.isfile(jsonFileName):
    with open(jsonFileName, "r") as fr:
        last_pycost_version_dict= json.load(fr)
else:
    last_pycost_version_dict= {'last_pycost_git_version':str(__version__), 'beta':0, 'last_git_short_hash':0}
    with open(jsonFileName, "w") as fw:
        json.dump(last_pycost_version_dict, fw)

def get_pycost_version():
    pycost_git_version= __version__
    last_pycost_git_version= last_pycost_version_dict['last_pycost_git_version']
    beta= int(last_pycost_version_dict['beta'])
    if(pycost_git_version != last_pycost_git_version):
        beta+= 1
    pycost_git_short_hash= get_git_revision_short_hash()
    last_pycost_git_short_hash= last_pycost_version_dict['last_git_short_hash']
    if(pycost_git_short_hash != last_pycost_git_short_hash):
        beta+= 1
    major_minor= pycost_git_version.split('.')
    major= major_minor[0]
    minor= major_minor[1]
    retval= major+'.'+minor+'.'+str(beta)
        
    return retval

if __name__ == '__main__':
    print(get_pycost_version())
