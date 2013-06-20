from fabric.api import *


env.hosts = ['v2v',]
env.use_ssh_config = True


@task
def pull():
    with cd('~/webapps/django_gu/v2v'):
        run('git pull')


@task
def build_static():
    run('django-admin.py collectstatic')
    with cd('~/webapps/django_gu/v2v/vacant_to_vibrant/collected_static/js/'):
        run('r.js -o app.build.js')


@task
def install_requirements():
    with cd('~/webapps/django_gu/v2v'):
        run('pip install -r requirements/base.txt')
        run('pip install -r requirements/production.txt')


@task
def migrate():
    run('django-admin.py migrate')


@task
def restart_django():
    run('supervisorctl -c ~/supervisor/supervisord.conf restart django')


@task
def status():
    run('supervisorctl -c ~/supervisor/supervisord.conf status')


@task
def deploy():
    pull()
    install_requirements()
    migrate()
    build_static()
    restart_django()
