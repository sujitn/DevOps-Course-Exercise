#!/bin/bash

gunicorn -b 0.0.0.0 --forwarded-allow-ips='*' 'app:create_app()'
