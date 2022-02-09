#!/bin/bash

code_path=#PATH#

if [[ "$OSTYPE" == "darwin"* ]]; then
    # MacOS
    python3 "$code_path/kbase-git.py" $@
else
    # Linux
    echo Running keybase service...
    run_keybase 1> /dev/null
    if [ $? -eq 0 ]; then
        sleep 2s
        python3 "$code_path/kbase-git.py" $@
    else
        echo [!] Could not start keybase service, is keybase installed?
        exit 1
    fi
fi