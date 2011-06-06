#!/usr/bin/env python

import imp
import os
import subprocess
import sys
import yaml

from optparse import OptionParser
from random import choice

from django.conf import settings
from django.template import Context
from django.template.loader import get_template


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

    site_domain = 'com'
    
    if not config['settings'].get('ignore_domain'):
        if '.' in site_name:
            site_name, site_domain = site_name.rsplit('.', 1)
    
    # add site name, port, and other vars to the config before loading up project
    # directories
    config['settings'].update({
        'site_name': site_name,
        'site_domain': site_domain,
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

def write_template(template_name, dest, context, safe=False):
    """
    given a template name, a destination, and a context,
    write a rendered template version to dest
    """
    filename = dest % context
    if os.path.isfile(filename) and safe:
        print 'Found %s, exiting' % filename
    else:
        t = get_template(template_name)
        contents = t.render(context)
        f = open(filename, 'w')
        print "Writing %s" % (filename)
        f.write(contents)
        f.close()

        if '.' in filename:
            base, ext = filename.rsplit('.', 1)
            if ext.lower() in ('sh', 'fcgi'):
                os.chmod(filename, 0755)

if __name__ == '__main__':
    parser = OptionParser(usage='%prog SITENAME [options]')
    parser.add_option('-t', '--templates', dest='templates', default=False,
                      help='Only copy template files', action='store_true')
    parser.add_option('-s', '--safe', dest='safe', default=False,
                      help='Do not overwrite any files encountered', action='store_true')
    parser.add_option('-f', '--framework', dest='framework', default='django',
                      help='type of site to create')
    parser.add_option('-p', '--port', dest='port', default='8080',
                      help='port to run site on (must be unused)')
    parser.add_option('--no-virtualenv', dest='novenv', default=False,
                      help='Do not create virtualenv for site', action='store_true')
    parser.add_option('--no-database', dest='nodb', default=False,
                      help='Do not attempt to create a database', action='store_true')
    parser.add_option('--no-copy', dest='nocp', default=False,
                      help='Do not attempt to copy any directories', action='store_true')
    parser.add_option('--no-pip', dest='nopip', default=False,
                      help='Do not attempt to install from requirements file', action='store_true')
    (options, args) = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(-1)
    
    current_dir = os.path.dirname(os.path.realpath(__file__))

    install_venv = not (options.novenv or options.templates)
    install_db = not (options.nodb or options.templates)
    should_copy = not (options.nocp or options.templates)
    install_pip = not (options.nopip or options.templates)

    # grap the site name and port it will run on from cmd line
    site_type = options.framework
    site_name = sys.argv[1]
    port = int(options.port)
    
    config = configure(site_type, site_name, port)
    
    file_mapping = config['files'] # destination: template
    staging_file_mapping = config.get('staging_files', {}) # destination: template
    directories = config['directories'] # list of shortcut: path
    copy_dirs = config['copy'] # dirs to copy into new env
    scripts = config.get('scripts', [])
    config = config['settings'] # move settings to top level
    
    install_venv = install_venv and config.get('virtualenv', True)
    
    # create a django context to use for rendering project templates
    context = Context(config)
    
    if install_venv:
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
        write_template(template_name, destination, context, options.safe)

    # write staging versions of the config files
    context['staging'] = True
    for destination, template_name in staging_file_mapping.items():
        write_template(template_name, destination, context, options.safe)

    if should_copy:
        flags = options.safe and '-nR' or '-R'
        for src, dest in copy_dirs.items():
            dest = dest % config
            print 'Copying %s' % src
            os.system('cp %s %s %s' % (flags, src, dest))

    if install_db and 'database' in config:
        print 'Creating database...' % context
        os.system(config['database'] % context)

    if install_pip and 'requirements_file' in config:
        pip_req = config['requirements_file']
        print 'Loading requirements from %s' % pip_req 
        os.system('pip install -E %s -r %s' % \
                  (context['site_root'], pip_req))
    
    if scripts:
        # allow arbitrary scripts to get executed at the end of processing
        scripts_dir = os.path.join(current_dir, site_type, 'scripts')
        print 'Loading scripts from %s' % scripts_dir
        
        for script in scripts:
            script_file = os.path.join(scripts_dir, script)
            print 'Executing "%s"' % script_file
            
            if script.endswith('.py'):
                try:
                    script_module = imp.load_source(script.split('.')[0], script_file)
                except ImportError:
                    print 'Error importing "%s" -- skipped' % script
                else:
                    hook = getattr(script_module, 'script_main', None)
                    if not hook:
                        print 'Error, "script_main" not found in script "%s"' % script
                    else:
                        hook(config)
            else:
                subprocess.call([script_file, context['site_name']])

    print 'Done!'
