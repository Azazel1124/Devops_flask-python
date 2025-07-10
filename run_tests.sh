#!/bin/bash

echo "Running tests for Flask application..."


pip install -r requirements.txt


python -m pytest tests/ -v --cov=.

echo "Tests completed!" 