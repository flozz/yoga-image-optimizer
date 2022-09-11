#!/bin/bash

# Print usage and exit if we have not arguments
if [ -z "$1" ] ; then
    echo "USAGE:"
    echo "  ./copy-data.sh <PREFIX>"
    echo
    echo "EXAMPLE:"
    echo "  ./copy-data.sh /usr"
    exit 1
fi

PREFIX=$(realpath $1)

# Go to the script directory
cd "${0%/*}" 1> /dev/null 2> /dev/null

# Copy desktop file
mkdir -pv $PREFIX/share/applications/
cp -v ./org.flozz.yoga-image-optimizer.desktop $PREFIX/share/applications/

# Copy icons
for size in 32 64 128 256 ; do
    mkdir -pv $PREFIX/share/icons/hicolor/${size}x${size}/apps/
    cp -v ../yoga_image_optimizer/data/images/icon_${size}.png \
          $PREFIX/share/icons/hicolor/${size}x${size}/apps/org.flozz.yoga-image-optimizer.png
done
mkdir -pv $PREFIX/share/icons/hicolor/scalable/apps/
cp -v ../yoga_image_optimizer/data/images/icon.svg \
      $PREFIX/share/icons/hicolor/scalable/apps/org.flozz.yoga-image-optimizer.svg

# Update icon cache for real installation
if [ $PREFIX == "/usr" ] ; then
    update-icon-caches /usr/share/icons/*
fi

# Copy man page
mkdir -pv $PREFIX/share/man/man1/
cp -v ./yoga-image-optimizer.1 $PREFIX/share/man/man1/yoga-image-optimizer.1
sed -i "s/{VERSION}/$(python3 ../setup.py --version)/g" $PREFIX/share/man/man1/yoga-image-optimizer.1

# Copy the Appstream file
mkdir -pv $PREFIX/share/metainfo/
cp -v ./org.flozz.yoga-image-optimizer.metainfo.xml $PREFIX/share/metainfo/org.flozz.yoga-image-optimizer.metainfo.xml
