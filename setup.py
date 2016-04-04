from setuptools import setup, find_packages

setup(
   name='cms50dplus',
   version='1.2',
   author='Asbj\xc3\xb8rn Brask',
   url='https://github.com/atbrask/CMS50Dplus',
   description='python interface for the cms50dplus pulse oximeter',
   packages=find_packages(),
   install_requires=['python-dateutil', 'pyserial']
)
