import os


def script_main(conf):
    os.chmod(os.path.join(conf['project_root'], 'manage.py'), 0755)
