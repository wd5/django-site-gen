#!/usr/bin/env python

import os
import sys
import yaml
from random import choice

from django.conf import settings
from django.template import Context
from django.template.loader import get_template

if len(sys.argv) < 3:
    print 'Usage: python generate_site.py [site_name] [port]'
    sys.exit(-1)

# grap the site name and port it will run on from cmd line
site_name, port = sys.argv[1], sys.argv[2]

# configure script to use templates in the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))
settings.configure(
    TEMPLATE_DIRS=(current_dir,),
)

# load the configuration file
fh = open('conf.yaml', 'r')
config = yaml.load(fh)

file_mapping = config['files'] # destination: template
local_file_mapping = config['local_files'] # destination: template
directories = config['directories'] # list of shortcut: path

config = config['settings']
fh.close()

# shhh!
secret_key = secret_key = ''.join([choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])

# add site name, port, and other vars to the config before loading up project
# directories
config.update({
    'site_name': site_name,
    'port': port,
    'local': False,
    'secret_key': secret_key,
})

# directories stored as list of dicts to enable sorting generic -> more specific
# i.e. site_root --> project_root --> media dir
for directory_dict in directories:
    for k, v in directory_dict.items():
        config[k] = v % config

# context used when rendering templates
context = Context(config)

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

print 'Creating database %(site_name)s_main' % context
os.system('createdb %(site_name)s_main' % context)

print 'Copying media directory'
os.system('cp -R ./media/* %(media)s' % context)

print 'Copying template directory'
os.system('cp -R ./templates/* %(templates)s' % context)

print 'Symlinking wsgi directory to site root'
os.system('cd %(site_root)s && ln -s %(wsgi)s' % context)

if 'requirements_file' in config:
    pip_req = config['requirements_file']
    print 'Loading requirements from %s' % pip_req 
    os.system('pip install -E %s -r %s' % \
              (context['site_root'], pip_req))

print 'Done!'
