#!/bin/bash

echo Running keybase service...
run_keybase 1> /dev/null
sleep 2s
if [ $? -eq 0 ]; then
    code_path=#PATH#
    python3 "$code_path/kbase-git.py" $@
else
    echo [!] Could not start keybase service, is keybase installed?
    exit 1
fi
