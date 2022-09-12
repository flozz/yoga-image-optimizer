Things to do while releasing a new version
==========================================

This file is a memo for the maintainer.


0. Checks
---------

* Check the locales list is up to date in ``winbuild/clean-gtk.sh``
* Check Copyright years in the About dialog
* Check screenshot links in ``linuxpkg/org.flozz.yoga-image-optimizer.metainfo.xml``


1. Release
----------

* Update version number in ``setup.py``
* Update version number in ``yoga_image_optimizer/__init__.py``
* Add release in ``linuxpkg/org.flozz.yoga-image-optimizer.metainfo``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


2. Build the Windows version
----------------------------

Follow instructions in `winbuild/ <./winbuild/README.rst>`_.

.. NOTE::

   Sadly there is no automated build yet for the Windows version. This should
   be done by hand in a clean Windows VM.


3. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

→ Automated :)


4. Publish the Flatpak package
------------------------------

Package repo: https://github.com/flathub/org.flozz.yoga-image-optimizer

* Update commit **tag and hash** in org.flozz.yoga-image-optimizer.yml
* Update dependencies (``./update-dependencies.sh``)
* Test the package:

  * Install the SDK: ``flatpak install flathub org.freedesktop.Sdk//21.08``
  * Install the runtime: ``flatpak install flathub org.freedesktop.Platform//21.08``
  * Build/install: ``flatpak-builder --force-clean --install --user build org.flozz.yoga-image-optimizer.yml``
  * Run: ``flatpak run --user org.flozz.yoga-image-optimizer``
  * Clean ``flatpak remove --user org.flozz.yoga-image-optimizer``

* Publish: commit / tag (``git commit -m vX.Y.Z && git tag vX.Y.Z && git push && git push --tags``)


5. Publish Github Release
~~~~~~~~~~~~~~~~~~~~~~~~~

* Make a release on Github
* Add changelog
* Add Windows Zip and Installer files to the release
