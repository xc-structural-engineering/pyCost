#!/bin/sh

echo "Installing pyCost."
export PYCOST_VERSION=$(python version.py)
export SYS_ARCH=$(dpkg --print-architecture)
export PYCOST_DEB_PKG_FOLDER="./debian-pkg"
export USR_LOCAL="/usr/local"
export PYCOST_INSTALLATION_TARGET="${PYCOST_DEB_PKG_FOLDER}${USR_LOCAL}/tmp"
echo "$PYCOST_VERSION" > ./pycost_installation_target.txt
echo "$SYS_ARCH" >> ./pycost_installation_target.txt
echo "$PYCOST_DEB_PKG_FOLDER" >> ./pycost_installation_target.txt
echo "$PYCOST_INSTALLATION_TARGET" >> ./pycost_installation_target.txt
echo "$USR_LOCAL" >> ./pycost_installation_target.txt
rm -rf $PYCOST_DEB_PKG_FOLDER
mkdir $PYCOST_DEB_PKG_FOLDER

pip3 install . -v --quiet --log ./installation_report.log --upgrade --target=$PYCOST_INSTALLATION_TARGET
python prepare_deb_pkg.py
# Create debian package
dpkg-deb --build $PYCOST_DEB_PKG_FOLDER
dpkg-name --overwrite "$PYCOST_DEB_PKG_FOLDER.deb"
PYCOST_DEB_PKG=$(ls -t *.deb | head -1)
echo "New Debian package: $PYCOST_DEB_PKG"
echo "Clean temporary files."
rm -r $PYCOST_DEB_PKG_FOLDER
echo "Install package."
sudo dpkg -i "$PYCOST_DEB_PKG"
echo "$PYCOST_DEB_PKG" >> ./pycost_installation_target.txt
echo "Remove package files after installation."
rm -vi *.deb

# Install required packages using pip3
pip3 install -r requirements.txt

