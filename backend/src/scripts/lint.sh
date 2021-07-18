#!/bin/bash

echo "Running mypy..."
mypy app --implicit-reexport

echo "\nRunning black..."
black app --check

echo "\nRunning isort..."
isort --check-only app

echo "\nRunning flake8..."
flake8 app