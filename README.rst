YOGA Image Optimizer
====================

|GitHub| |License| |Discord| |Github Actions| |Black|

**YOGA Image Optimizer** is a graphical user interface for `YOGA Image <https://github.com/wanadev/yoga>`_ that **converts and optimizes** the size of **JPEG, PNG and WebP** image files.

.. figure:: ./screenshot.png
   :alt: YOGA Image Optimizer screenshot


Requirements
------------

* PyCairo
* PyGObject ≥ 3.36
* Python ≥ 3.7
* YOGA ≥ 1.1.0


Installation
------------

Arch Linux
~~~~~~~~~~

The package is available on AUR (``yoga-image-optimizer``):

* https://aur.archlinux.org/packages/yoga-image-optimizer


Flatpak (Linux)
~~~~~~~~~~~~~~~

A Flatpak package is available on Flathub. This is currently the simplest way to install YOGA Image Optimizer on all major Linux distributions:

* https://flathub.org/apps/details/org.flozz.yoga-image-optimizer


Linux (PyPI)
~~~~~~~~~~~~

You must install the dependencies on your system first. It can be done via the following command on Debian and Ubuntu::

    sudo apt install git build-essential python3 python3-dev python3-pip libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0

Then install YOGA Image Optimizer with pip::

    sudo pip3 install yoga-image-optimizer

**NOTE:** Installing from PyPI will not install ``.desktop`` file and manual page; you will not be able to run the software from your graphical app menu (GNOME Shell etc.).


Linux (source)
~~~~~~~~~~~~~~

You must install the dependencies on your system first. It can be done via the following command on Debian and Ubuntu::

    sudo apt install git build-essential python3 python3-dev python3-pip libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0

Then clone this repository and navigate to it::

    git clone https://github.com/flozz/yoga-image-optimizer.git
    cd yoga-image-optimizer

Then install YOGA Image Optimizer using pip::

    sudo pip3 install .

Finally, you can install the ``.desktop`` file, icons and manual page using the following command::

    sudo ./linuxpkg/copy-data.sh /usr


Windows
~~~~~~~

Download either the portable .zip version or the Windows installer from the releases page:

* https://github.com/flozz/yoga-image-optimizer/releases


Usage
-----

Just type the following command to run YOGA Image Optimizer::

    yoga-image-optimizer

You can also give some image files to open::

    yoga-image-optimizer  image1.png  image2.jpeg


**NOTE:** If you installed YOGA Image Optimizer from Flathub, you will have to run the following command instead::

    flatpak run org.flozz.yoga-image-optimizer  image1.png  image2.jpeg


Contributing
------------

Questions
~~~~~~~~~

If you have any question, you can:

* `Open an issue <https://github.com/flozz/yoga-image-optimizer/issues>`_ on GitHub
* `Ask on Discord <https://discord.gg/P77sWhuSs4>`_ (I am not always available to chat, but I try to answer to everyone)


Bugs
~~~~

Please `open an issue <https://github.com/flozz/yoga-image-optimizer/issues>`_ on GitHub with as much information as possible if you found a bug:

* Your operating system / Linux distribution (and its version)
* How you installed the software
* All the logs and message outputted by the software
* etc.


Pull requests
~~~~~~~~~~~~~

Please consider `filing a bug <https://github.com/flozz/yoga-image-optimizer/issues>`_ before starting to work on a new feature; it will allow us to discuss the best way to do it. It is obviously unnecessary if you just want to fix a typo or small errors in the code.

Please note that your code must follow the coding style defined by the `pep8 <https://pep8.org>`_ and pass tests. `Black <https://black.readthedocs.io/en/stable>`_ and `Flake8 <https://flake8.pycqa.org/en/latest>`_ are used on this project to enforce the coding style.


Translate YOGA Image Optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can help translating it if the software is not available on your language.

To translate YOGA Image Optimizer, you can:

* Submit your translations creating a pull request on GitHub
* Translate online via `POEditor <https://poeditor.com/join/project/RoQ2r9rv89>`_

If you submit your translations with a pull request on GitHub. Do not forget to add your name as the translation of the ``translator-credits`` key (one name per line, email is optional)::

    #: yoga_image_optimizer/about_dialog.py:38
    msgid "translator-credits"
    msgstr ""
    "John DOE\n"
    "Other TRANSLATOR <foobar@example.org>\n"


Run the tests
~~~~~~~~~~~~~

You must install `Nox <https://nox.thea.codes/>`__ first::

    pip3 install nox

Then you can check for lint error::

    nox --session lint

or run the tests::

    nox --session test

You can use following commands to run the tests only on a certain Python version (the corresponding Python interpreter must be installed on your machine)::

    nox --session test-3.7
    nox --session test-3.8
    nox --session test-3.9
    nox --session test-3.10
    nox --session test-3.11

You can also fix coding style errors automatically with::

    nox -s black_fix


Build, extract or update build translations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You must install `Nox <https://nox.thea.codes>`__ first::

    pip3 install nox

To extract messages and update locales, run::

    nox --session locales_update

To compile locales, run::

    nox --session locales_compile

**NOTE:** you must have ``msgfmt``, ``msgmerge`` and ``xgettext`` executable installed on your system to run the above commands. It can be done via the following command on Debian and Ubuntu::

    sudo apt install gettext


Support this project
--------------------

Want to support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__
* `💵️ Give me a tip on PayPal <https://www.paypal.me/0xflozz>`__
* `❤️ Sponsor me on GitHub <https://github.com/sponsors/flozz>`__


Changelog
---------

* **[NEXT]** (changes on ``master``, but not released yet):

  * Nothing yet ;)

* **v1.2.2:**

  * Bug fix:

    * Fixed an issue that prevents the update of the view with older Pango
      versions (@flozz, #41)

  * Translations:

    * Updated Italian translation (@albanobattistella, #39)
    * Updated Spanish translation (@haggen88, #42)

* **v1.2.1:**

  * Fixes / improvements:

    * Flatpak: use the real user cache, not the one of the Flatpak application
      (@flozz)
    * Added Python 3.11 support (@flozz)

  * Translations:

    * Added Brazilian Portuguese translation (@Kazevic, #36)
    * Completed Dutch translation (@Vistaus, #34)

* **v1.2.0:**

  * Interface / user experience:

    * More compact and less bloated interface (#17)
    * Allow opening input images in the default image viewer by double-clicking
      them
    * Asynchronous generation and loading of thumbnails to not freeze the
      interface when importing a lot of images (#26)
    * Sped up thumbnail loading on Linux by using already generated thumbnails
      from the shared cache
    * Sped up thumbnail generation using BOX sampling instead of LANCZOS
    * Show a warning icon if the output image is larger than the input one

  * Fixes / improvements:

    * Fixed a crash when generating thumbnails for JPEGs with an invalid
      orientation EXIF tag (#29)
    * Fixed a crash on the image import process when generating a broken
      image's thumbnail (#27)
    * Fixed a crash on the optimization batch if an error occurs when
      optimizing an image (#27)
    * Fixed inverted width and height with rotated JPEGs
    * Fixed issues related to ``concurrent.futures`` on Python 3.7 and 3.8
      (#32)
    * Updated the code to not use deprecated constants on newer Pillow versions

  * New translations:

    * Dutch (incomplete) (@Vistaus, #25)
    * German (Jürgen Benvenuti)

* **v1.1.2:**

  * New translations:

    * Russian
    * Spanish

  * Updated translation:

    * Turkish

* **v1.1.1:**

  * Fixed the abnormal amount of processes created and not cleaned when
    starting an optimization (#13)

* **v1.1.0:**

  * `YOGA <https://github.com/wanadev/yoga>`_ updated to v1.1.0:

    * Honor the JPEG orientation EXIF tag
    * JPEG optimization improved: up to 7.3% of additional size reduction since
      previous version
    * YOGA can no more output a PNG larger than the input one when performing
      a PNG to PNG optimization

  * Added a setting window:

    * Number of threads used to optimize images
    * Setting the default output locations / name or pattern of output files
    * Theme selection / dark theme preference

  * "Optimize" and "Stop" buttons behaviour improved:

    * The "Stop" button now stops the running optimizations, not just the
      pending ones
    * Display a "Canceled" status on non-optimized image while the "Stop"
      button is clicked
    * Do not optimize again images that have already been optimized

  * Allow to resize images (downscale only, preserve ratio)

  * Multiselection: multiple files can now be selected and their parameters can
    be edited all at once (multiselection)

  * Windows specific changes:

    * Use the Adwaita theme by default on Windows; the Windows10 GTK theme
      looks buggy

  * Fixes / improvements:

    * Do not allow to remove images with the ``<Del>`` key while an
      optimization is in progress
    * Fixed image previews; no more ugly thumbnails with indexed images
    * Image previews now honor the JPEG orientation EXIF tag

  * Updated translations:

    * French
    * Italian (partial)
    * Occitan
    * Turkish (partial)

  * **Note for packagers:**

    * YOGA ≥ 1.1.0 is now needed
    * YOGA v1.1.0 has a new dependency: `mozjpeg-lossless-optimization
      <https://github.com/wanadev/mozjpeg-lossless-optimization>`_

* **v1.0.1:**

  * Fixed PyPI packages
  * **NOTE:** No new version for Windows; nothing changed

* **v1.0.0:**

  * Fixed ``[-]`` button not removing the chosen image
  * Updated site URL

* **v0.99.2 (beta):**

  * Fixed package data not installed while installing with pip (#3)
  * **NOTE:** No new version for Windows; nothing changed

* **v0.99.1 (beta):**

  * Fixed site URL in setup.py
  * Fixed version number

* **v0.99.0 (beta):**

  * Initial release
  * Linux and Windows support
  * Optimizes JPEG, PNG and WebP image formats


.. |GitHub| image:: https://img.shields.io/github/stars/flozz/yoga-image-optimizer?label=GitHub&logo=github
   :target: https://github.com/flozz/yoga-image-optimizer

.. |License| image:: https://img.shields.io/github/license/flozz/yoga-image-optimizer
   :target: https://github.com/flozz/yoga-image-optimizer/blob/master/COPYING

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |Github Actions| image:: https://github.com/flozz/yoga-image-optimizer/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/yoga-image-optimizer/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable
