#!/usr/bin/env bash
service nginx start
cd src || exit
gunicorn --access-logfile=/leian_proxy/access.log --log-level debug -m 007 -w 4 wsgi:app