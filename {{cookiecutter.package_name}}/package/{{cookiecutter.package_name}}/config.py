from dynaconf import Dynaconf
from . import PACKAGE_NAME

from importlib.resources import path

with path(PACKAGE_NAME, 'config.py') as this_file:
    settings = Dynaconf(
        root_path=this_file.parent,
        settings_files=["settings.toml", "{{cookiecutter.package_name}}.secrets.toml"],
    )
