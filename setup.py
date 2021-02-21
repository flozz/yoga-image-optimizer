#!/usr/bin/env python
# encoding: UTF-8

import os

from setuptools import setup, find_packages


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r").read()


setup(
    name="yoga_image_optimizer",
    version="0.0.0",
    description="A graphical interface to optimizes JPEG and PNG images",
    url="https://github.com/wanadev/yoga",
    license="BSD-3-Clause",

    long_description=long_description,
    keywords="image jpeg png optimizer converter guetzli zopfli gui gtk",  # noqa

    author="Fabien LOISON",

    packages=find_packages(),

    install_requires=[
        "yoga>=0.11.0",
        ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
        ]},

    entry_points={
        "console_scripts": [
            "yoga-image-optimizer = yoga_image_optimizer.__main__:main"
        ]},

    )
