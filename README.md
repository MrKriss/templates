# templates
cookiecutter templates for data science and development

## Requirements

* Python 3.7
* [cookiecutter](https://github.com/audreyr/cookiecutter). Can be installed with `pip install cookiecutter`
* [invoke](http://www.pyinvoke.org/). Can be installed with `pip install invoke`

## Basic Usage

    cookiecutter <clone_url_for_this_git_repo>

i.e.

    cookiecutter git@ssh.dev.azure.com:v3/frontier-analytics/Data%20Science/package-template

* Folder layout for python package project
* Post processing hooks to create a new conda environment with the latest version of given Python libraries
* Also optionally create a git repo and commit the initial project contents
