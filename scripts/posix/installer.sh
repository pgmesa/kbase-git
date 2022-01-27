#!/bin/bash

python3 ./../.path.py --replace

sudo cp ./kbase-git.sh /usr/local/bin/kbase-git

python3 ./../.path.py --reset
