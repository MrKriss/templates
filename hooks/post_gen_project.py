""" Post Project Generation Hooks 

1. Create a new conda environment with the latest version of libraries specified
2. Also, if specified, create a git repo and commit the project contents

"""

import subprocess
import shlex

# The string in these variables will be overriden by cookiecutter
PROJECT_NAME = "{{cookiecutter.project_name | lower | replace(' ', '_')}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"
GIT_USAGE = "{{cookiecutter.git_usage}}" == "Yes"

# Create the strings for commands to run, substituting with the values from cookiecutter
conda_install_cmd = ("conda env create -f dev_environment.yml")
conda_save_env_cmd = f"conda env export -n {PROJECT_NAME} -f frozen_environment.yml"

# Execute command with subprocess module
print(f'--------------------------------- Installing conda environment for {PROJECT_NAME} ...')
subprocess.run(shlex.split(conda_install_cmd))
print(f'------------------------ Finished installing conda environment for {PROJECT_NAME}')

print('---------------- Saving snapshot of conda environment to "frozen_environment.yml" ... ')
subprocess.run(shlex.split(conda_save_env_cmd))
print(f'---------------- Finished saving snapshot of conda environment for {PROJECT_NAME}')

# If using git, initialise the repo.
if GIT_USAGE:
    print(f'-------- Initialising git repo and creating initial commit for {PROJECT_NAME} ...')
    subprocess.run(shlex.split('git init'))
    subprocess.run(shlex.split('git add *'))
    subprocess.run(shlex.split('git commit -m "Initial commit of project template"'))
    print(f'--------------------------- Finished initialising git repo for {PROJECT_NAME}')
