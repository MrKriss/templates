# -*- coding: utf-8 -*-
""" Sample setup.py file for a Python Library 

This is a minimal example of what to include when registering a command line function
to call the library.
"""

from setuptools import setup, find_packages

setup(
    name='{{cookiecutter.package_name}}',
    version='0.1.0',
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests', 'examples']),
    # This next section registers 'mycommand' as a command line utility that will execute 
    # the `command_line_entry_point()` function in the `command_line` module of `mypackage`
    entry_points={
        'console_scripts': ['{{cookiecutter.clf_name}}={{cookiecutter.package_name}}.command_line:command_line_entry_point']
    }, 
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov']

)



