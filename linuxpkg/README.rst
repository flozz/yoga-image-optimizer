Packaging YOGA Image Optimizer on Linux
=======================================

In addition to the Python package itself, you will find in this folder various
useful files for Linux packaging, such as .desktop file to launch the
application or a manual file.

This folder also contains a script to copy all required files (desktop, icons
and manual) at the right location.

USAGE::

    ./copy-data.sh <PREFIX>

Where ``<PREFIX>`` is the prefix directory for the installation. For a real
installation, the prefix will be ``/usr``::

    ./copy-data.sh /usr

For a package, it may be your package's build folder::

    ./copy-data.sh /tmp/build-package/usr
