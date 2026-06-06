#!/usr/bin/env python

from setuptools import setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="relations-postgresql",
    version="0.6.3",
    package_dir = {'': 'lib'},
    py_modules = [
        'relations_postgresql',
        'relations_postgresql.sql',
        'relations_postgresql.expression',
        'relations_postgresql.criterion',
        'relations_postgresql.criteria',
        'relations_postgresql.clause',
        'relations_postgresql.query',
        'relations_postgresql.ddl',
        'relations_postgresql.column',
        'relations_postgresql.index',
        'relations_postgresql.table'
    ],
    install_requires=[
        'relations-sql>=0.6.8'
    ],
    url="https://github.com/relations-dil/python-relations-postgresql",
    author="Gaffer Fitch",
    author_email="relations@gaf3.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license_files=('LICENSE.txt',),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)
