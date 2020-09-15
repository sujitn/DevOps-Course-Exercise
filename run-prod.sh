#!/bin/bash

gunicorn -b 0.0.0.0 'app:create_app()'