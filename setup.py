
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'msp430dll',
    version = '1.0',
    description = 'MSP430DLL (Python wrapper for msp430.dll).',
    long_description = long_description,
    url = 'https://github.com/christoph2/msp430dll',
    author = 'Christoph Schueler',
    author_email = 'cpu12.gems@googlemail.com',
    license = 'GPL',
    classifiers = [
        'Development Status :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords = 'msp430 microcontroller [development]',
    packages = find_packages(exclude = ['contrib', 'docs', 'tests']),
    install_requires = [u'enum34'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require = {
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data = {
        'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    #data_files=[('my_data', ['data/data_file'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'msp430-info = msp430dll.msp430_info:main',
        ],
    },
    test_suite="msp430dll.tests"
)
