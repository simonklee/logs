# -*- coding: utf-8 -*-
r"""
Logs
----

Analyzing uwsgi logs
"""

import sys
import os

from setuptools import setup
from distutils.command.build_ext import build_ext
from distutils.errors import CCompilerError, DistutilsExecError, \
    DistutilsPlatformError
try:
    import multiprocessing
except ImportError:
    pass

cmdclass = {}

class BuildFailed(Exception):
    pass

ext_errors = (CCompilerError, DistutilsExecError, DistutilsPlatformError)

class ve_build_ext(build_ext):
    """This class allows C extension building to fail."""

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError:
            raise BuildFailed()

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except ext_errors:
            raise BuildFailed()

cmdclass['build_ext'] = ve_build_ext
speedups = None

def run_setup(with_binary):
    features = {}
    if with_binary and speedups is not None:
        features['speedups'] = speedups

    setup(
        name='logs',
        version='0.2.1',
        license='MIT',
        url='https://github.com/simonz05/logs/',
        author='Simon Zimmermann',
        author_email='simon@insmo.com',
        description='Logs',
        long_description=__doc__,
        keywords="logs",
        platforms='any',
        packages=['logs'],
        package_data={'logs': ['data']},
        scripts=['bin/log.py'],
        cmdclass=cmdclass,
        features=features,
        install_requires=['numpy'],
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: POSIX",
            "Programming Language :: Python",
            "Topic :: Software Development",
            "Topic :: Software Development :: Libraries",
        ],
    )

def echo(msg=''):
    sys.stdout.write(msg + '\n')

try:
    run_setup(True)
except BuildFailed:
    LINE = '=' * 74
    BUILD_EXT_WARNING = ('WARNING: The C extension could not be compiled, '
                         'speedups are not enabled.')

    echo(LINE)
    echo(BUILD_EXT_WARNING)
    echo('Failure information, if any, is above.')
    echo('Retrying the build without the C extension now.')
    echo()

    run_setup(False)

    echo(LINE)
    echo(BUILD_EXT_WARNING)
    echo('Plain-Python installation succeeded.')
    echo(LINE)
