#!/bin/bash
gunicorn --config /gunicorn-cfg.py wsgi:app
