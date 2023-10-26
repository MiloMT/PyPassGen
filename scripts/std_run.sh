# Script to run a standard configuration from a standard environment.

#!/bin/bash

# Check that python command exists.
if ! [[ -x "$(command -v python)" ]]
then
    echo "Error:
This program runs on Python, but it looks like Python is not installed.
To install python, check out https://www.python.org/" >&2
    exit 1
fi

# Array to check args against
arg_array=("std" "view" "exp")

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
        if [[ $1 == "std" ]]
        then
            # Standard run executes app with 10 chars and 5 passwords.
            python3 ../__main__.py 10 5
            exit 0
        elif [[ $1 == "view" ]]
        then
            # View run executes the app in view mode
            python3 ../__main__.py --view
            exit 0
        elif [[ $1 == "exp" ]]
        then
            # Expression run executes the app in expression mode while 
            # generating 5 passwords of length 10 characters
            python3 ../__main__.py 10 5 -e
            exit 0
        elif [[ $# -eq 0 ]]
        then
            # Standard run if no bash script arguments passed.
            python3 ../__main__.py 10 5
            exit 0
        elif ! [[ ${arg_array[*]} =~ $1 ]]
        then
            # If the argument is invalid, will exit and provide to user valid
            # prompts
            echo "Error:
The argument you have passed to the script is invalid. The list
of valid arguments is:
    - std: For a standard configuration run.
    - exp: To run the app in expression mode.
    - view: To run the app in view mode." >&2
            exit 1
        fi
    fi
fi

# Only runs if above python version checks fails.
echo "Error:
A minimum of Python 3.10 needs to be installed to run this application.
To install python, check out https://www.python.org/" >&2
exit 1