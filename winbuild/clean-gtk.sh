#!/bin/bash

# Remove debug symbols
find yoga-image-optimizer.dist/gtk -iname "*.pdb" -delete

# Remove compilation-time dependencies (unlinked lib, headers,...) and tests
find yoga-image-optimizer.dist/gtk -iname "*.lib" -delete
find yoga-image-optimizer.dist/gtk -iname "*.a" -delete
find yoga-image-optimizer.dist/gtk -iname "*.h" -delete
rm -rf yoga-image-optimizer.dist/gtk/include
rm -rf yoga-image-optimizer.dist/gtk/lib/pkgconfig
rm -rf yoga-image-optimizer.dist/gtk/lib/{cmake,glib-2.0,gobject-introspection,gtk-3.0,libpng,pkgconfig}
rm -rf yoga-image-optimizer.dist/gtk/share/gir-1.0  # This is compiled in lib/girepository-1.0
rm -rf yoga-image-optimizer.dist/gtk/share/{aclocal,gobject-introspection-1.0,installed-tests,pkgconfig}
rm -rf yoga-image-optimizer.dist/gtk/libexec

# Remove parts of the Adwaita theme we do not use such as cursors
rm -rf yoga-image-optimizer.dist/gtk/share/icons/Adwaita/cursors

# Remove all useless .exe
rm -f yoga-image-optimizer.dist/gtk/bin/*.exe
