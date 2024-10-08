# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright (C) 2009-2012  Luis C. Pérez Tato
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See https://github.com/lcpt/pyCost or email : l.pereztato@gmail.com
#

from setuptools import setup
from setuptools import find_packages
import sys
import version

# Get version
pycost_version= version.__version__
pycost_deb_pkg_folder= None
pycost_installation_target= None
usr_local_pth= None
with open('./pycost_installation_target.txt','r') as f:
    pycost_version= f.readline().strip()
    sys_arch= f.readline().strip()
    pycost_deb_pkg_folder= f.readline().strip()
    pycost_installation_target= f.readline().strip()
    usr_local_pth= f.readline().strip()
if (pycost_version is None):
    logging.error('PYCOST_VERSION not set.')
    exit(1)
if (sys_arch is None):
    logging.error('SYS_ARCH not set.')
    exit(1)
if (pycost_deb_pkg_folder is None):
    logging.error('PYCOST_DEB_PKG_FOLDER not set.')
    exit(1)
if (pycost_installation_target is None):
    logging.error('PYCOST_INSTALLATION_TARGET not set.')
    exit(1)
if (usr_local_pth is None):
    logging.error('USR_LOCAL not set.')
    exit(1)

pycost_packages= ['pycost','pycost.bc3','pycost.measurements','pycost.prices','pycost.prices.price_justification','pycost.structure','pycost.utils','pycost.utils.structural_members']

print('pyCost temporary folder: '+pycost_deb_pkg_folder)
print('pyCost temporary installation target: '+pycost_installation_target)

setup(name='pycost',
      version= pycost_version,
      author='Luis C. Pérez Tato',
      packages= find_packages(include= pycost_packages),
      install_requires=[],
      data_files=[]
     )
