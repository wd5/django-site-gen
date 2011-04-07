django-site-gen
===============

a utility script for generating skeleton django sites (and now support
for other frameworks like flask).


What it creates
---------------

assuming a base directory of /home/user/envs/, django-site-gen
will create the following when executed like so::

    python generate_site.py twitter.com -p 9001

.. image:: http://charlesleifer.com/media/images/photos/django-site-gen.png


using for flask
^^^^^^^^^^^^^^^

if you want to use the flask framework, django-site-gen will
create the following::

    python generate_site.py twitter.com -p 9001 -f flask

* envs/twitter/ - the root directory of flask site - a virtualenv
* envs/twitter/conf/ - gunicorn and nginx confs for local and production
* envs/twitter/logs/ - gunicorn and nginx logs
* envs/twitter/twitter/ - where the site and sqlite db live
* envs/twitter/twitter/static/ - site media served by nginx
* envs/twitter/twitter/templates/ - site template dirs
