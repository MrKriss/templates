""" Hooks to create a new conda environment with the latest version of common libraries 

Also optionally create a git repo and commit the project contents
"""

import subprocess
import shlex

# The string in these variables will be overriden by cookiecutter
PROJECT_NAME = "{{cookiecutter.project_name|lower|replace(' ', '_')}}"
PYTHON_LIBRARIES = "{{cookiecutter.python_libraries}}"

# Create the strings for commands to run, substituting with the values from cookiecutter
conda_install_cmd = f"conda create -y -n {PROJECT_NAME} python=3 {PYTHON_LIBRARIES}"

conda_save_env_cmd = f"conda env export -n {PROJECT_NAME} -f environment.yml"

# Execute command with subprocess module
print(f'Installing conda environment for {PROJECT_NAME} ...' )
subprocess.run(shlex.split(conda_install_cmd))
print(f'Finished installing conda environment for {PROJECT_NAME}')

print('Saving snapshot of conda environment to "environment.yml" ... ', end='')
subprocess.run(shlex.split(conda_save_env_cmd))
print('Complete!')


# If using git, initialise the rep.
# The code in this following Jinja2 block only gets inserted when "use_git" is set to Yes
{% if cookiecutter.use_git == "Yes" %}
print(f'Initialising Git repo and creating initial commit for {PROJECT_NAME} ...')
subprocess.run(shlex.split('git init'))
subprocess.run(shlex.split('git add *'))
subprocess.run(shlex.split('git commit -m "Initial commit of project template"'))
print("Complete!!!")
{% endif %}
