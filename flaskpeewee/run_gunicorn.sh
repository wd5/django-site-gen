#!/bin/sh
gunicorn main:app -c ./conf/staging/gunicorn.conf.py
