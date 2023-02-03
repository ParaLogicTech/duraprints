# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in duraprints/__init__.py
from duraprints import __version__ as version

setup(
	name='duraprints',
	version=version,
	description='App to automate complex order booking and production cycle',
	author='Betalogics',
	author_email='avaiskhatri@betalogics.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
