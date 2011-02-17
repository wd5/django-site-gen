#!/bin/sh
gunicorn app:app -c ./conf/staging/gunicorn.conf.py
