#!/bin/bash

echo "Running autoflake..."
autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
echo "\n"

echo "Running black"
black app
echo "\n"

echo "Running isort"
isort app -p app/

