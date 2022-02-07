#!/bin/bash

code_path=#PATH#

echo Searching for updates...
git -C "$code_path" pull origin main

python3 "$code_path/kbase-git.py" $@