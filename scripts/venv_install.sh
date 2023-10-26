# Script to install PyPassGen dependencies to virtual environment

#!/bin/bash

# Check that python command exists.
if ! [[ -x "$(command -v python)" ]]
then
    echo "Error:
This program runs on Python, but it looks like Python is not installed.
To install python, check out https://www.python.org/" >&2
    exit 1
fi

# Break python version into array.
long_pyversion=$(python --version)
short_pyversion=${long_pyversion:7}
IFS='.' read -r -a split_pyversion <<< "$short_pyversion"

# Ensure python main version is 3.
if [[ ${split_pyversion[0]} == 3 ]]
then
    # Ensure python subversion is minimum 3.10.
    if [[ ${split_pyversion[1]} > 10 ]]
    then
        # If a venv folder doesn't already exist, than create a venv
        if ! [[ -d "../.venv" ]]
        then
            python -m venv ../.venv
            echo "A virtual environment has been created as a '.venv' folder"
            echo ""
            source ../.venv/bin/activate
        # Else if it does exist, just activate venv and install to existing
        elif [[ -d "../.venv" ]]
        then
            echo "You already have an existing '.venv' folder. The existing"
            echo "Virtual environment will be used to install dependencies"
            echo ""
            source ../.venv/bin/activate
        fi
        # Install package dependencies
        echo "Packages to be installed:"
        echo "------------------------------"
        pip install -r ../requirements.txt
        echo "------------------------------"
        echo "Dependencies have been successfully installed"
        echo "Please run the 'venv_run.sh' script to use application"
        deactivate
        exit 0
    fi
fi

# Only runs if above python version checks fails.
echo "Error:
A minimum of Python 3.10 needs to be installed to run this application.
To install python, check out https://www.python.org/" >&2
exit 1