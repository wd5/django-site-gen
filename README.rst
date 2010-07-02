django-site-gen
===============

a utility script for generating skeleton django sites

it's still pretty tied to my workflow, so check back as I hope to be
making it more generic.


What it creates
---------------

assuming a base directory of /home/user/envs/, django-site-gen
will create the following when executed like so::

    python generate_site.py twitter 9001

* envs/twitter/ - the root directory of django site - a virtualenv
* envs/twitter/apache/ - where the wsgi file lives
* envs/twitter/conf/ - apache and nginx confs for local and production
* envs/twitter/logs/ - apache and nginx logs
* envs/twitter/twitter/ - where the site, site apps, settings, etc live
* envs/twitter/twitter/media/ - site media served by nginx
* envs/twitter/twitter/templates/ - site template dirs
