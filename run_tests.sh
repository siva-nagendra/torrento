#!/bin/bash

# Run Black
echo "Running Black..."
black --check . || black .
echo "Black completed."

# Run Pylint
echo "Running Pylint..."
pylint torrento.py || (echo "Pylint found issues, attempting to auto-fix..." && autopep8 --in-place --aggressive --aggressive torrento.py && pylint torrento.py)
echo "Pylint completed."

# Check for 'quiet' argument
if [[ $1 == "quiet" ]]; then
    echo "Running tests in quiet mode..."
    pytest tests -q 
else
    echo "Running tests in verbose mode..."
    pytest tests -v
fi

echo "Testing completed."
