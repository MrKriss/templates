# -*- coding: utf-8 -*-
""" Sample setup.py file for a Python Library

This is a minimal example of what to include when registering a command line function
to call the library.
"""

from setuptools import setup, find_packages

setup(
    name="{{cookiecutter.package_name}}",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=["docs", "tests", "examples"]),
    # Include the settings.toml file when installing the package
    package_data={"": ["settings.toml"]},
    install_requires=[
        "dynaconf",
        "pydantic",
        "loguru",
{%- for lib in cookiecutter.python_libraries.strip().split() %}
    {%- if lib != "NONE" %}
        "{{lib}}",
    {%- endif %}
{%- endfor %}
    ],
    # Versioning is based on the git repo tag, see https://pypi.org/project/setuptools-scm/
    use_scm_version={
        "root": "..",
        "relative_to": __file__,
        "write_to": "package/{{cookiecutter.package_name}}/version.py",
    },
)
