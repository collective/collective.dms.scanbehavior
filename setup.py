# -*- coding: utf-8 -*-
"""Installer for the collective.dms.scanbehavior package."""

from setuptools import find_packages
from setuptools import setup


long_description = (
    open("README.rst").read() + "\n" + "Contributors\n"
    "============\n"
    + "\n"
    + open("CONTRIBUTORS.rst").read()
    + "\n"
    + open("CHANGES.rst").read()
    + "\n"
)


setup(
    name="collective.dms.scanbehavior",
    version="1.3.2.dev0",
    description="Behavior adding scan metadata",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="Python Zope Plone",
    author="Franck NGAHA, Stephan Geulette",
    author_email="franck.o.ngaha@gmail.com, sgeulette@imio.be",
    url="http://pypi.python.org/pypi/collective.dms.scanbehavior",
    license="GPL",
    packages=find_packages("src"),
    namespace_packages=["collective", "collective.dms"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "plone.api",
        "setuptools",
        "plone.app.dexterity",
        "plone.behavior",
        "zope.schema",
        "zope.interface",
        "zope.component",
        "rwproperty",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.robotframework[debug]",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
