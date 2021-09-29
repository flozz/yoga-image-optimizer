YOGA Image Optimizer
====================

|Github| |Discord| |Github Actions| |Black| |License|

**YOGA Image Optimizer** is a graphical user interface for `YOGA Image <https://github.com/wanadev/yoga>`_ that **converts and optimizes** the size of **JPEGs, PNGs and WebP** image files.

.. figure:: ./screenshot.png
   :alt: YOGA Image Optimizer screenshot


Requirements
------------

* Python >= 3.7,
* YOGA >= 1.1.0,
* PyCairo,
* PyGObject >= 3.36,


Install
-------

ArchLinux
~~~~~~~~~

The package is available on AUR (``yoga-image-optimizer``):

* https://aur.archlinux.org/packages/yoga-image-optimizer/

Flatpak (Linux)
~~~~~~~~~~~~~~~

A Flatpak package is available on Flathub. This is currently the simplest way to install YOGA Image Optimizer on all major Linux distributions:

* https://flathub.org/apps/details/org.flozz.yoga-image-optimizer

Linux (source)
~~~~~~~~~~~~~~

First, you will need to install some dependencies on your system. On Debian and Ubuntu this can be achieved with the following command::

    sudo apt install git build-essential python3 python3-dev python3-pip libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0

Then clone this repository and navigate to it::

    git clone https://github.com/flozz/yoga-image-optimizer.git
    cd yoga-image-optimizer

Then install YOGA Image Optimizer using pip::

    sudo pip3 install .

Finally, you can install desktop file, icons and manual using the following command::

    sudo ./linuxpkg/copy-data.sh /usr

Linux (PyPI)
~~~~~~~~~~~~

First, you will need to install some dependencies on your system. On Debian and Ubuntu this can be achieved with the following command::

    sudo apt install git build-essential python3 python3-dev python3-pip libgirepository1.0-dev libcairo2-dev pkg-config gir1.2-gtk-3.0

Then install YOGA Image Optimizer using pip::

    sudo pip3 install yoga-image-optimizer

**NOTE:** Installing from PyPI will not install ``.desktop`` file and man page. You will not be able to run the software from your graphical app menu (GNOME Shell,...).

Windows
~~~~~~~

Download either the portable .zip version or the Windows installer from the release page:

* https://github.com/flozz/yoga-image-optimizer/releases


Usage
-----

To run YOGA Image Optimizer, just type the following command::

    yoga-image-optimizer

You can also pass some image files to open::

    yoga-image-optimizer  image1.png  image2.jpeg


Contributing
------------

Questions
~~~~~~~~~

If you have any question, you can:

* `open an issue <https://github.com/flozz/yoga-image-optimizer/issues>`_ on Github,
* or `ask on Discord <https://discord.gg/P77sWhuSs4>`_ (I am not always available for chatting but I try to answer to everyone).

Bugs
~~~~

If you found a bug, please `open an issue <https://github.com/flozz/yoga-image-optimizer/issues>`_ on Github with as much information as possible:

* What is your operating system / Linux distribution (and its version),
* How you installed the software,
* All the logs and message outputted by the software,
* ...

Pull Requests
~~~~~~~~~~~~~

Please consider `filing a bug <https://github.com/flozz/yoga-image-optimizer/issues>`_ before starting to work on a new feature. This will allow us to discuss the best way to do it. This is of course not necessary if you just want to fix some typo or small errors in the code.

Please note that your code must pass tests and follow the coding style defined by the `pep8 <https://pep8.org/>`_. `Flake8 <https://flake8.pycqa.org/en/latest/>`_ and `Black <https://black.readthedocs.io/en/stable/>`_ are used on this project to enforce coding style.

Translating YOGA Image Optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the software is not available in your language, you can help translating it.

To translate YOGA Image Optimizer, you can submit your translations using a Pull Request on Github. Do not forget to add your name as the translation of the ``translator-credits`` key (one name per line, e-mail is optional)::

    #: yoga_image_optimizer/about_dialog.py:38
    msgid "translator-credits"
    msgstr ""
    "John DOE\n"
    "Other TRANSLATOR <foobar@example.org>\n"


Running The Tests
~~~~~~~~~~~~~~~~~

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

Then you can check for lint error::

    nox --session lint

or run the tests::

    nox --session test

To run the tests only for a specific Python version, you can use following commands (the corresponding Python interpreter must be installed on your machine)::

    nox --session test-3.7
    nox --session test-3.8
    nox --session test-3.9

You can also fix automatically coding style errors with::

    nox -s black_fix

Extract, Update or Build Translations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You will first have to install `nox <https://nox.thea.codes/>`_::

    pip3 install nox

To extract messages and update locales run::

    nox --session locales_update

To compile locales, run::

    nox --session locales_compile

**NOTE:** you will need to have ``xgettext``, ``msgmerge`` and ``msgfmt`` executable installed on your system to run the above commands. On Debian / Ubuntu, they can be installed with the following command::

    sudo apt install gettext


Supporting this project
-----------------------

Wanna support this project?

* `☕️ Buy me a coffee <https://www.buymeacoffee.com/flozz>`__,
* `❤️ sponsor me on Github <https://github.com/sponsors/flozz>`__,
* `💵️ or give me a tip on PayPal <https://www.paypal.me/0xflozz>`__.


Changelog
---------

* **[NEXT]** (changes on ``master`` but not released yet):

  * Nothing yet

* **v1.1.1:**

  * Fix the abnormal amount of processes created (and not cleaned) when
    starting an optimization (#13)

* **v1.1.0:**

  * `YOGA <https://github.com/wanadev/yoga>`_ updated to v1.1.0:

    * Honor the JPEG orientation EXIF tag
    * JPEG optimization improved: up to 7.3 % of additional size reduction
      since previous version.
    * YOGA can no more output a PNG larger than the input one when performing
      a PNG to PNG optimization

  * Settings were added:

    * Theme selection / dark theme preference
    * Number of threads used to optimize images
    * Setting the default output locations / name or pattern of output files

  * "Optimize" and "Stop" buttons behaviour improved:

    * The "Stop" button now stops the running optimizations and not only the
      pending ones
    * Display a "Canceled" status on non-optimized image while the "Stop"
      button is clicked
    * Do not optimize again images that have already been optimized

  * Allow to resize images (downscale only, preserve ratio)

  * Multiselection: Multiple files can now be selected and their parameters can
    be edited all at once

  * Bug fix / improvements:

    * Do not allow to remove images with the ``<Del>`` key while an
      optimization is in progress
    * Fix image previews: no more ugly thumbnails with indexed images
    * Image previews now honor the JPEG orientation EXIF tag

  * Windows specific changes:

    * Use the Adwaita theme by default on Windows as the Windows10 GTK theme
      looks buggy

  * Translations udpated:

    * French
    * Italian (partial)
    * Occitan
    * Turkish (partial)

  * **NOTE for packagers:**

    * YOGA >= 1.1.0 is now required
    * YOGA v1.1.0 requires a new dependency: `mozjpeg-lossless-optimization
      <https://github.com/wanadev/mozjpeg-lossless-optimization>`_

* **v1.0.1:**

  * Fix PyPI packages
  * NOTE: no new release for Windows as nothing changed

* **v1.0.0:**

  * Fix ``[-]`` button do not remove selected image
  * Update site URL

* **v0.99.2 (beta):**

  * Fix package data not installed while installing with pip (#3)
  * NOTE: no new release for Windows as nothing changed

* **v0.99.1 (beta):**

  * Fix site URL in setup.py
  * Fix version number

* **v0.99.0 (beta):**

  * Initial release
  * Linux and Windows support
  * Optimizes PNG, JPEG and WebP image formats


.. |Github| image:: https://img.shields.io/github/stars/flozz/yoga-image-optimizer?label=Github&logo=github
   :target: https://github.com/flozz/yoga-image-optimizer

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |Github Actions| image:: https://github.com/flozz/yoga-image-optimizer/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/yoga-image-optimizer/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/

.. |License| image:: https://img.shields.io/github/license/flozz/yoga-image-optimizer
   :target: https://github.com/flozz/yoga-image-optimizer/blob/master/COPYING
