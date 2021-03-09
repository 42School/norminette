#!/bin/bash

SUFFIX="V3"

if [ "$#" -gt "0" ]
then
	SUFFIX="-dev"
fi

BUILD_DIR="build"
BUNDLE_DIR="bundle"
PKG_ROOT="$BUILD_DIR/pkgroot"
PACKAGE_NAME="norminette$SUFFIX"
DESCRIPTION="Norminette"
VERSION=`cat norminette/__init__.py | grep version | cut -d'"' -f2`
OUTFILE="norminette_$SUFFIX_$VERSION.pkg"
SUBDIRECTORY="apps/norminette"

rm -rf $BUILD_DIR $BUNDLE_DIR
mkdir $BUILD_DIR $BUNDLE_DIR
python3 -m venv $BUILD_DIR/venv
source $BUILD_DIR/venv/bin/activate
python3 setup.py install
sed -i '' 's#\#\!\/.*norminette.*/venv#\#\!/usr/local/share/norminetteV3/venv#' $BUILD_DIR/venv/bin/*
deactivate

mkdir -p $PKG_ROOT/usr/local/share/$PACKAGE_NAME
mv $BUILD_DIR/venv $PKG_ROOT/usr/local/share/$PACKAGE_NAME/venv

pkgbuild --identifier $PACKAGE_NAME --version $VERSION --root $PKG_ROOT --install-location / $BUNDLE_DIR/$OUTFILE

rm -rf $BUILD_DIR dist/
