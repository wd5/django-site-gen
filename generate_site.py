#!/usr/bin/env python

import os
import sys
import yaml
from random import choice

from django.conf import settings
from django.template import Context
from django.template.loader import get_template

DEFAULT_TYPE = 'django'


def configure(site_type, site_name, port, config_file='conf.yaml'):
    # configure script to use templates in the current directory
    current_dir = os.path.dirname(os.path.realpath(__file__))
    current_dir = os.path.join(current_dir, site_type)
    settings.configure(
        TEMPLATE_DIRS=(current_dir,),
    )
    
    # set current working dir to current_dir
    os.chdir(current_dir)

    # load the configuration file
    fh = open(config_file, 'r')
    config = yaml.load(fh)
    fh.close()
    
    # shhh!
    secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    
    # add site name, port, and other vars to the config before loading up project
    # directories
    config['settings'].update({
        'site_name': site_name,
        'port': port,
        'local': False,
        'secret_key': secret_key,
    })

    # directories stored as list of dicts to enable sorting generic -> more specific
    # i.e. site_root --> project_root --> media dir
    for directory_dict in config['directories']:
        for k, v in directory_dict.items():
            config['settings'][k] = v % config['settings']

    return config

def write_template(template_name, dest, context):
    """
    given a template name, a destination, and a context,
    write a rendered template version to dest
    """
    t = get_template(template_name)
    contents = t.render(context)
    f = open(dest % context, 'w')
    print "Writing %s" % (dest % context)
    f.write(contents)
    f.close()

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 2:
        args.insert(0, DEFAULT_TYPE)

    if len(args) < 3:
        print 'Usage: python generate_site.py [site_type] [site_name] [port]'
        sys.exit(-1)

    # grap the site name and port it will run on from cmd line
    site_type, site_name, port = args[:3]
    
    config = configure(site_type, site_name, port)
    
    file_mapping = config['files'] # destination: template
    local_file_mapping = config.get('local_files', []) # destination: template
    directories = config['directories'] # list of shortcut: path
    copy_dirs = config['copy'] # dirs to copy into new env
    config = config['settings'] # move settings to top level
    
    # create a django context to use for rendering project templates
    context = Context(config)
    
    # create a new virtualenv for the project
    print 'Creating a virtualenv for the project'
    os.system('cd %(base_site)s && virtualenv --no-site-packages %(site_name)s' % context)

    # create the directory structure for the site
    for directory_dict in directories:
        for k, v in directory_dict.items():
            try:
                os.makedirs(v % context)
            except OSError, e:
                if e.errno != 17:
                    raise

    # write all files
    for destination, template_name in file_mapping.items():
        write_template(template_name, destination, context)

    # write local versions of the config files
    context['local'] = True
    for destination, template_name in local_file_mapping.items():
        write_template(template_name, destination, context)

    for src, dest in copy_dirs.items():
        dest = dest % config
        print 'Copying %s' % src
        os.system('cp -R %s %s' % (src, dest))

    if 'database' in config:
        print 'Creating database...' % context
        os.system(config['database'] % context)

    if 'requirements_file' in config:
        pip_req = config['requirements_file']
        print 'Loading requirements from %s' % pip_req 
        os.system('pip install -E %s -r %s' % \
                  (context['site_root'], pip_req))

    print 'Done!'
