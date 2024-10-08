# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright (C) 2024  Luis C. Pérez Tato
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
# See http://www.xcingenieria.com/ or email : l.perez@xcingenieria.com
#

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AO_O)"
__copyright__= "Copyright 2024, LCPT and AO_O"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com" "ana.ortega.ort@gmail.com"

import os
import logging
import platform
import site
import apt

def locate_dependencies(dependencies):
    ''' Find the APT packages in the given list when available and, if not,
        put them in a requirements string.

    :returns: depends_string, requirements_string; the first string containes
              a line to declare the Debian package dependencies and the
              second one the information to write in the 'requirements.txt'
              file for its later use with pip3.
    '''
    apt_available= list()
    not_apt_available= list()

    cache= apt.Cache()
    for dep in dependencies:
        versions= list()
        if(dep in cache):
            pkg= cache[dep]
            versions= pkg.versions
        if(len(versions)>0):
            apt_available.append(dep)
        else:
            not_apt_available.append(dep)

    if(len(apt_available)>0):
        depends_string= 'Depends: '+ apt_available[0]
        if(len(apt_available)>1):
            for pkg in apt_available[1:]:
                depends_string+= ', '+pkg

    requirements_string= '###### pyCost requirements ######\n'
    pkg_prefix= 'python3-'
    for pkg in not_apt_available:
        if(pkg.startswith(pkg_prefix)):
            pkg= pkg[8:]
        requirements_string+= pkg+'\n'
    return depends_string, requirements_string

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
    
# Get site packages.
site_packages= site.getsitepackages()
pth_to_libs= None
for pth in site_packages:
    if(pth.startswith(usr_local_pth)):
        pth_to_libs= pth
if (pth_to_libs is None):
    logging.error('Can\'t find: '+str(usr_local_pth)+' among site packages.')
    exit(1)
else:
    pth_to_libs= pycost_deb_pkg_folder+pth_to_libs
    print('path to libs: ', pth_to_libs)
    with open("./pycost_installation_target.txt","a") as f:
        f.write(pth_to_libs+'\n')

# Locate dependencies.
dependencies= ['python3', 'python3-num2words', 'python3-pylatex']
depends_string, requirements_string= locate_dependencies(dependencies)

with open('./requirements.txt', 'w') as f:
    f.write(requirements_string)
    
print('depends_string: "'+depends_string+'"')
print('\nrequirements_string: "'+requirements_string+'"')

# Prepare Debian package folder.
## Create DEBIAN directory
cmd= 'mkdir '+pycost_deb_pkg_folder+'/DEBIAN/'
os.system(cmd)
### Create control file.
control_file_contents= '''Package: pycost-python-modules
Version: pycost_version
Architecture: sys_arch
Maintainer: Luis C. Pérez Tato <l.pereztato@gmail.com>
Description: Python modules of the pyCost that allows to calculate the "bill of quantites" of a project (in an AEC context).
'''
#### Set version.
control_file_contents= control_file_contents.replace('pycost_version', pycost_version)
#### Get architecture.
machine= platform.machine()
control_file_contents= control_file_contents.replace('sys_arch', sys_arch)
#### Dependencies.
control_file_contents+= depends_string+'\n'
print('*****', control_file_contents)

control_file_path= pycost_deb_pkg_folder+'/DEBIAN/control'
with open(control_file_path, 'w') as f:
    f.write(control_file_contents)
postinst_file_name= pycost_deb_pkg_folder+'/DEBIAN/postinst'
cmd= 'touch '+postinst_file_name
os.system(cmd)
os.chmod(postinst_file_name, 0o755)
# Move Python modules to the corresponding Python packages folder
cmd= 'mkdir -p '+pth_to_libs
os.system(cmd)
origin= pycost_installation_target+'/*'
dest= pth_to_libs
cmd= 'mv '+origin+' '+dest
os.system(cmd)
print('cmd= ', cmd)
cmd= 'rmdir '+ pycost_installation_target
os.system(cmd)
print('cmd= ', cmd)

