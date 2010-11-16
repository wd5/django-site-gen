#!/bin/sh
gunicorn app:app -c ./conf/gunicorn.conf.py
