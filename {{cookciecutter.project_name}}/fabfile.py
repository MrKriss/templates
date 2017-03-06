
from fabric.api import cd, env, lcd, put, sudo, run, path, local
from fabric.contrib.files import exists

##############
#   config   #
##############

project_name = '{{cookiecutter.project_name}}'

local_app_dir = f'./{project_name}'
local_config_dir = './config'

remote_app_dir = '/home/www'
# remote_git_dir = '/home/git'
remote_flask_dir = f'{remote_app_dir}/{project_name}'
remote_nginx_dir = '/etc/nginx/sites-enabled'
remote_supervisor_dir = '/etc/supervisor/conf.d'

env.hosts = ['{{cookiecutter.remote_host}}']  # replace with IP address or hostname
env.user = '{{cookiecutter.remote_username}}'

miniconda_dir = '{{cookiecutter.miniconda_dir}}'
remote_flask_env = f'{miniconda_dir}/envs/{project_name}'

#############
#   tasks   #
#############


def install_miniconda():
    """ Install Latest Miniconda Python Distribution """
    if exists(miniconda_dir) is False:
        sudo('wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh')
        sudo(f"bash Miniconda3-latest-Linux-x86_64.sh -p {miniconda_dir} -b")
        sudo("rm Miniconda3-latest-Linux-x86_64.sh")


def install_requirements():
    """ Install required system level packages. """
    sudo('apt-get update')
    sudo('apt-get install -y git')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y python')  # Need system python for supervisor as its 2.x only
    # sudo('apt-get install -y python-pip')
    # sudo('apt-get install -y python-virtualenv')
    # sudo('apt-get install -y gunicorn')
    install_miniconda()
    with path(f'{miniconda_dir}/bin'):
        run('conda install -yq gunicorn')


def install_flask():
    """ Install the Flask Application + Dependencies

    1. Create project directories
    2. Create conda env if not created
    3. Update conda env with requirements.txt
    4. Copy Flask files to remote host
    """
    # Initialise Project Directories
    if exists(remote_app_dir) is False:
        sudo('mkdir ' + remote_app_dir)
    if exists(remote_flask_dir) is False:
        sudo('mkdir ' + remote_flask_dir)

    # Use requirements.txt to create / update the conda env
    req_path = '/tmp/files/requirements.txt'
    sudo('mkdir -p /tmp/files')
    put('./requirements.txt', req_path, use_sudo=True)

    with path(f'{miniconda_dir}/bin'):
        if exists(remote_flask_env) is False:
            run(f'conda create -yq -n {project_name} --file {req_path}')
        else:
            run(f'conda update -yq -n {project_name} --file {req_path}')

    # Copy Flask Application Files to Remote Host
    with lcd(local_app_dir):
        with cd(remote_flask_dir):
            put('*', './', use_sudo=True)


def configure_nginx():
    """ Configure nginx reverse proxy server

    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    # Remove Default config 
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')
    # Create New Config
    if exists(f'/etc/nginx/sites-enabled/{project_name}') is False:
        sudo(f'touch /etc/nginx/sites-available/{project_name}')
        # Setup Symbolic Link
        sudo(f'ln -s /etc/nginx/sites-available/{project_name}' +
             f' {remote_nginx_dir}/{project_name}')
    # Copy local config to remote config
    with lcd(local_config_dir):
        with cd(remote_nginx_dir):
            put(f'./{project_name}', './', use_sudo=True)
    # Restart nginx
    sudo('/etc/init.d/nginx restart')


def configure_supervisor():
    """ Setup Supervisord process
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """

    if exists(f'/etc/supervisor/conf.d/{project_name}.conf') is False:
        sudo('service supervisor start')
        with lcd(local_config_dir):
            with cd(remote_supervisor_dir):
                put(f'./{project_name}.conf', './', use_sudo=True)
                sudo('supervisorctl reread')
                sudo('supervisorctl update')


def run_app():
    """ Run the app! """
    with cd(remote_flask_dir):
        sudo(f'supervisorctl start {project_name}')


def deploy():
    """
    1. Copy new Flask files
    2. Restart gunicorn via supervisor
    """
    # Copy Flask Application Files to Remote Host
    with lcd(local_app_dir):
        with cd(remote_flask_dir):
            put('*', './', use_sudo=True)

    sudo(f'supervisorctl restart {project_name}')


def rollback():
    """
    1. Quick rollback in case of error
    2. Restart gunicorn via supervisor
    """
    with lcd(local_app_dir):
        local('git revert master  --no-edit')
        with cd(remote_flask_dir):
            put('*', './', use_sudo=True)
        sudo(f'supervisorctl restart {project_name}')


def status():
    """ Is our app live? """
    sudo('supervisorctl status')


def create():
    install_requirements()
    install_flask()
    configure_nginx()
    configure_supervisor()
