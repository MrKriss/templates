
.PHONY:freeze update rolback

# Save new snapshot of environment 
freeze: 
	conda env export -n {{cookiecutter.project_name}} -f frozen_environment.yml

# Load/update env based on latest version of libraries in dev_environment file
update:
	conda env update -n {{cookiecutter.project_name}} -f dev_environment.yml

# Reset env based on frozen version of libraries in frozen_environment file
rollback:
	conda env remove -n {{cookiecutter.project_name}}
	conda env create -n {{cookiecutter.project_name}} -f frozen_environment.yml

# Run all numbered notebooks in sequence, updating them inpace
run-notebooks:
	find -s ./analysis -name "[0-9][0-9]*.ipynb" -print0 | xargs -0 -I {} jupyter nbconvert --to notebook --execute {}
