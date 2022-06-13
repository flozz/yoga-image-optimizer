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

# Remove all useless .exe
cd yoga-image-optimizer.dist/gtk/bin
mkdir bak
mv gdbus.exe bak/
mv gspawn-win64-helper.exe bak/
rm *.exe
mv bak/*.exe .
rmdir bak
cd -

# Adwaita icon theme: keep only what we use
cd yoga-image-optimizer.dist/gtk/share/icons/
mkdir -p Adwaita.keep/scalable/actions
mkdir -p Adwaita.keep/scalable/ui
mkdir -p Adwaita.keep/scalable/status
for icon in actions/list-add-symbolic \
            actions/list-remove-symbolic \
            actions/value-increase-symbolic \
            actions/value-decrease-symbolic \
            actions/edit-delete-symbolic \
            actions/open-menu-symbolic \
            actions/edit-undo-symbolic \
            actions/view-more-symbolic \
            ui/window-close-symbolic \
            ui/window-maximize-symbolic \
            ui/window-minimize-symbolic \
            ui/window-restore-symbolic \
            ui/pan-up-symbolic \
            ui/pan-down-symbolic \
            status/dialog-question-symbolic
do
    mv Adwaita/scalable/$icon.svg Adwaita.keep/scalable/$icon.svg
done
cp Adwaita/index.theme Adwaita.keep/index.theme
rm -rf Adwaita
mv Adwaita.keep Adwaita
cd -

# Keep only supported locales
cd yoga-image-optimizer.dist/gtk/share/
mkdir -p locale.keep
for l10n in fr en it oc tr es ru
do
    mv locale/$l10n locale.keep/$l0n
done
rm -r locale
mv locale.keep locale
cd -
