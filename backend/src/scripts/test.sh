#!/bin/bash

set -e

echo "Running pytest..."
pytest --ds=app.system.settings.test -vv -p conftest --cov=app --cov-config=.coveragerc --cov-report=term-missing app "${@}"
