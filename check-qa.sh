#!/bin/sh
#
# Check QA
#

# compile all python files
python -m compileall -f -x '/(local|.git)/' -q .

# pass unit tests
python -m unittest discover

# comply with PEP8
pep8 --exclude '.git,local,settings_*' .
pep8 settings_sample.py
