from setuptools import setup, find_packages
# To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='engarde',

    version='0.0.2',

    description='A python package for defensive data analysis.',
    long_description='A python package for defensive data analysis.',

    url='https://github.com/tomaugspurger/engarde',

    # Author details
    author='Tom Augspurger',
    author_email='tom.w.augspurger@gmail.com',

    # Choose your license
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='data analysis',
    packages=find_packages(exclude=['tests']),
    # install_requires=['numpy', 'pandas'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [''],
        'test': ['coverage', 'pytest'],
    },

)
