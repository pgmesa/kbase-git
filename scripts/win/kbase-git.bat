@echo off

set code_path=#PATH#

echo Searching for updates...
git -C "%code_path%" pull origin main 

py "%code_path%\kbase-git.py" %*
