from setuptools import setup, find_packages

setup(
    name='netro-api-python',
    version='blue',
    description='Netro API',
    description='this package contains a Netro API python wrapper',
    packages=find_packages(exclude=('tests*', 'testing*', 'doc*')),
    url='https://github.com/kcofoni/netro-api-python.git/',
    author='kcofoni',
    author_email='kcofoni@gmail.com',
)
