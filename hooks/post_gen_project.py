""" Hooks to create a new conda environment with the latest version of common libraries

Also optionally create a git repo and commit the project contents
"""

from invoke import run

# The string in these variables will be overriden by cookiecutter
PROJECT_NAME = "{{cookiecutter.package_name|lower|replace(' ', '-')|replace('_', '-')}}"
PYTHON_VERSION = "{{cookiecutter.python_version}}"
PYTHON_LIBRARIES = "{{cookiecutter.python_libraries}}"
USE_GIT = "{{cookiecutter.use_git}}" == "Yes"

# Create the strings for commands to run, substituting with the values from cookiecutter
conda_install_cmd = f"conda create -y -n {PROJECT_NAME} python={PYTHON_VERSION} {PYTHON_LIBRARIES}"

# Execute command with subprocess module
print(f"--------------------------------- Installing conda environment for {PROJECT_NAME} ...")
run(conda_install_cmd, echo=True, hide="out")
print(f"------------------------ Finished installing conda environment for {PROJECT_NAME}")

# If using git, initialise the rep.
# The code in this following Jinja2 block only gets inserted when "use_git" is set to Yes
if USE_GIT:
    print(f"-------- Initialising git repo and creating initial commit for {PROJECT_NAME} ...")
    run("git init", echo=True)
    run("git add *", echo=True)
    run('git commit -m "Initial commit of project template"', echo=True)
    run("git tag v0.1.0", echo=True)
    print(f"--------------------------- Finished initialising git repo for {PROJECT_NAME}")
