# This script will run unit tests and linting against the current code.
# The logic here is meant to mirror that contained in the GitHub workflow.

PROJECT_ROOT=../..

echo "Running unit tests"
pushd $PROJECT_ROOT
coverage run -m pytest
popd
coverage report -m

echo "Running linting tests"
pushd $PROJECT_ROOT
flake8
pushd 
