import os

from fabric.api import env, run, sudo
from fabric.context_managers import cd
from fabric.contrib.files import exists


env.user = 'fabric-user'
env.hosts = ['libservdhc7.princeton.edu']
env.repo = 'derrida-django'
env.gitbase = 'https://www.github.com/Princeton-CDH/'
env.build = 'develop'
env.deploy_prefix = '/var/deploy/'
env.web_prefix = '/var/www/'
env.deploy_dir = '%(deploy_prefix)s%(repo)s/' % env


# Requires the ***local*** location for the SSH key for the fabric user
# You can also load your key into an ssh-agent and bypass this step
# If queried for a password, fabric may actually be asking for the key pass.
# This is a known problem unfortunately.

# TODO: Break up the mile long command strings to something more legible.

# Add a private key file location to OS environment or load it in your ssh-agent
user_key = os.environ.get('FABRIC_KEY')

if user_key is not None:
    env.key_filename = user_key


# Use me to test your SSH and server settings!
def host_type():
    run('uname -s')


def deploy_qa(build=None, rebuild=False):
    '''Runs qa build using env dict
    kwargs:
    build -- git hash or overall branch name ('develop', 'master')
    rebuild -- Boolean, if True removes commit dir and rebuilds

    syntax:
    fab deploy_qa:build=<hash>

    '''

    if build is not None:
        env.build = build

    env.source_dir = '%(deploy_dir)ssource/' % env

    # Clone the git repo to a directory
    if not exists(env.deploy_prefix):
        sudo('mdkir %s' % env.deploy_prefix)
    if not exists(env.source_dir):
        sudo('mkdir %s' % env.source_dir)

    env.repo_dir = '%(source_dir)s%(repo)s' % env
    if not exists(env.repo_dir):
        with cd(env.source_dir):
            sudo('git clone %(gitbase)s%(repo)s.git' % env)

    with cd(env.repo_dir):
        output = sudo('git fetch origin && git checkout %(build)s' % env)
        # Check to make sure there are no untracked files
        sudo('git ls-files --other --directory --exclude-standard | sed q1')
        # Get the short hash and fast forward if we're on a branch
        # TODO: Better way for future deploys
        if 'fast-forwarded' in output:
            sudo('git pull origin %(build)s' % env)
        env.hash = sudo('git rev-parse --short HEAD')
    env.deploy_commit_dir = '%(deploy_dir)s%(repo)s-%(hash)s' % env

    if exists(env.deploy_commit_dir) and rebuild is False:
        # Reset symlinks for apache
        with cd('/var/www/'):
            if exists('%(repo)s' % env):
                sudo('rm -f %(repo)s' % env)
            sudo('ln -s %(deploy_commit_dir)s %(repo)s' % env)

    else:
        if exists(env.deploy_commit_dir):
            sudo('rm -rf %(deploy_commit_dir)s' % env)

        sudo('mkdir %(deploy_commit_dir)s' % env)
        sudo('cp -r %(repo_dir)s/* %(deploy_commit_dir)s/' % env)

        with cd(env.deploy_commit_dir):

            # Build venv in env/
            sudo('mkdir env')
            sudo('semanage fcontext -a -t httpd_sys_script_exec_t %(deploy_commit_dir)s/env' % env)
            sudo('restorecon -R -v env/')
            sudo('/var/deploy/build_env.sh')

            # Link local_settings.py for winthrop -- REPO SPECIFIC
            sudo('rm -f derrida/local_settings.py')
            sudo('ln -s /var/deploy/%(repo)s/local_settings.py derrida/local_settings.py' % env)

            # Backup mySQL and migrate+collectstatic
            # Uses two scripts deployed server-side per application
            # Avaiable in server scripts repo
            sudo('../make_dump.sh')
            sudo('../migrate_collect.sh')

        # Redo symlinks for apache
        with cd('/var/www/'):
            if exists('%(repo)s' % env):
                sudo('rm -f %(repo)s' % env)
            sudo('ln -s %(deploy_commit_dir)s/  %(repo)s' % env)

        # Set permissions and SELinux
        sudo('chown root:apache -R /var/deploy/ && chmod g+rwx -R /var/deploy')

        if rebuild is not False:
            # Do a restart because we had to rebuild a directory
            sudo('systemctl restart httpd24-httpd')
        else:
            # touch wsgi.py to trigger a reload
            sudo('touch %(web_prefix)s/%(repo)s/derrida/wsgi.py' % env)
