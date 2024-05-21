#!/bin/bash
# gunicorn --config /gunicorn-cfg.py wsgi:app
waitress-serve --listen=*:8000 wsgi:app
