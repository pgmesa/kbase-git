#!/bin/bash

python3 ./../.path.py --replace
if [ $? -eq 0 ]; then
    sudo cp ./kbase-git.sh /usr/local/bin/kbase-git
    python3 ./../.path.py --reset
else
    echo [!] Instalation failed
    exit 1
fi


