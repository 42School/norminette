#!/bin/bash

SUFFIX=""

if [ "$#" -gt "0" ]
then
	SUFFIX="-dev"
fi

BUILD_DIR="build"
PKG_ROOT="$BUILD_DIR/pkgroot"
PACKAGE_NAME="norminette$SUFFIX"
DESCRIPTION="Norminette"
VERSION=`cat norminette/version.py | cut -d'"' -f2`
OUTFILE="norminette_$VERSION$SUFFIX.pkg"
SUBDIRECTORY="apps/norminette"

rm $OUTFILE

rm -rf $BUILD_DIR
mkdir $BUILD_DIR
python3 -m venv $BUILD_DIR/venv
source $BUILD_DIR/venv/bin/activate
python3 setup.py install
sed -i '' 's#/Users/.*/venv#/usr/share/norminette/venv#' $BUILD_DIR/venv/bin/*
deactivate

mkdir -p $PKG_ROOT/usr/share/norminette
mv $BUILD_DIR/venv $PKG_ROOT/usr/share/norminette/venv

pkgbuild --identifier $PACKAGE_NAME --version $VERSION --root $PKG_ROOT --install-location / $OUTFILE
rm -rf $BUILD_DIR
rm -rf dist


