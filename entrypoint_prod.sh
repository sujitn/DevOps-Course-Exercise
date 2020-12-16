#!/bin/bash

gunicorn -b 0.0.0.0:$PORT --forwarded-allow-ips='*' 'app:create_app()'
