#!/bin/bash

sudo rm /usr/local/bin/kbase-git
if [ $? -eq 0 ]; then
    echo [%] Uninstalation Succeeded
else
    echo [!] Uninstalation Failed
    exit 1
fi
