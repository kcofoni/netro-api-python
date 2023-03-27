from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
   
    name='netro-api-python',
    version='0.2',
    description='Netro API',
    long_description=long_description,

    packages=find_packages(exclude=('tests', 'docs')),
    
    #The project's main homepage.
    url='https://github.com/kcofoni/netro-api-python.git/',

    # Author details
    author='kcofoni',
    author_email='kcofoni@gmail.com',

    license='MIT',

    keywords = ['Netro'],
    classifiers=[],


)
