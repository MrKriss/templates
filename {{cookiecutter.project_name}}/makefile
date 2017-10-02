
ENV_NAME = {{cookiecutter.project_name|lower|replace(' ', '_')}}

.PHONY:save load update

# Save new snapshot of environment 
save: 
	conda env export -n $(ENV_NAME) -f environment.yml

# Load/update env based on environment file
load: 
	conda env update -n $(ENV_NAME) -f environment.yml

# Uninstall environment 
remove: 
	conda env remove -n $(ENV_NAME)

