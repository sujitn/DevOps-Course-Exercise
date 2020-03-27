#!/bin/bash

echo "Starting test runner..."
watchmedo auto-restart --recursive --directory="." --pattern="*.py" --ignore-patterns="*/.*" pytest
