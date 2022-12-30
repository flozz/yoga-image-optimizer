#!/usr/bin/env python
# encoding: UTF-8

import os

from setuptools import setup, find_packages


long_description = ""
if os.path.isfile("README.rst"):
    long_description = open("README.rst", "r", encoding="UTF-8").read()


setup(
    name="yoga_image_optimizer",
    version="1.2.2",
    description="A graphical interface to convert and optimize JPEG, PNG and WebP images (based on YOGA)",
    url="https://yoga.flozz.org/",
    project_urls={
        "Source Code": "https://github.com/flozz/yoga-image-optimizer",
        "News": "https://yoga.flozz.org/#news",
        "Issues": "https://github.com/flozz/yoga-image-optimizer/issues",
        "Chat": "https://discord.gg/P77sWhuSs4",
        "Donate": "https://github.com/flozz/yoga-image-optimizer#support-this-project",
    },
    license="GPLv3",
    long_description=long_description,
    keywords="image jpeg png optimizer converter guetzli zopfli gui gtk",
    author="Fabien LOISON",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "yoga>=1.1.0",
        "pycairo",
        "PyGObject>=3.26",
    ],
    extras_require={
        "dev": [
            "nox",
            "flake8",
            "pytest",
            "black",
        ]
    },
    entry_points={
        "console_scripts": [
            "yoga-image-optimizer = yoga_image_optimizer.__main__:main",
        ]
    },
)
