#!/bin/bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:${PORT:-10000} app:app
