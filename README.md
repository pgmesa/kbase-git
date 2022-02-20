
# Kbase-Git (OS-Independent)

This program has been made for developers which are writing not open source code and don't want anyone to have access to it or don't wan't any platform to analyze their project, because has commercial purposes or must be secret for whatever reason. The idea is to use the free tool 'keybase' (https://keybase.io/download) for encrypting your data (not even they know what you store -> RSA encryption. Data is encrypted locally with public_key and then sent to the server). 

The program uses 'keybase' and 'git' command line interfaces to upload git projects automatically and periodically to keybase, so that if your computer is stolen, the source code will be encrypted in the keybase servers and not exposed in your computer, which is generally easy to hack and gain access to the information you have inside if someone puts effort in it.

Despite the fact that the best practice with this program is to upload manually the code when you have finished your work session (kbase-git upload), the program offers the abilitty to create automated tasks depending on the OS you are using, to ensure that the code is every day uploaded to keybase at the hours you have scheduled, in case you forgot to upload it manually.

This program is for securing the daily development of the project of each individual of the team, but for storing the git project to work with the team (as github does - push, clone, pull, fetch...) you can use keybase functionality to create encrypted repositories (read more about this in the keybase website - https://keybase.io/).

## Project Uploading
When uploading the project, all tracked files by git will be removed from your computer and then the .git folder will be moved to keybase. A log file will also be created in the "__logs__" directory.

When downloading the project, all files are restored from the .git with their original state (staged or not), leaving the git project as it was when the upload took place (same git logs, commits, added files...) 

## Supported OS
- Windows
- Linux [Debian based] (Don't have tested with other linux distributions)
- Mac

## Requirements
- Have KeyBase installed and be logged in
- Python >= 3.7
- It has no external dependencies so you don't have to install anything with pip (all integrated python modules)

## Keybase Configuration
- For it to work, you have to create a keybase account, and leave the option in settings to never log out enabled (if your computer is stolen, you can log out from another device and they can only access your data if they are connected to the internet (don't enable the option to sync data in your keybase folders, as this makes your keybase data accessible offline and we don't want that)).
- You also have to activate the option to open keybase on startup, so that it starts when you turn on the computer (it allows the program to interact with keybase without you touching anything)
- Normally these two options that I have mentioned are already activated by default, but just in case not, activate them

## Installation
- To access the script globally from any path and without having to run 'python ...' you have to run the installer corresponding to your operating system -> 'scripts/[win or posix]/installer[.bat or .sh ]' (posix = mac and linux) (in case of posix, execute permissions are already given to the files). The script will ask you for administrator permissions so that the 'kbase-git.[OS]' script can be copied to a path that is added to the default system PATH, 'C:\Windows\System32' (windows) and ' /usr/local/bin' (linux and mac).
- During installation, a file will be created in 'configs/[your keybase username].json' where you can put the paths you want to be uploaded directly to keybase (see 'example.json').
- A folder named 'kbase-git_uploads' will be created in 'keybase/private/[user-name]'
- To check that it is installed correctly, run 'kbase-git' from a command terminal to display the help of the program.

## How to use
    - 'upload': "Uploads the .git folder to keybase and removes the project locally, -g for configured paths in .json",
    - 'download': "Downloads the .git folder from keybase and restores the project, -g for configured paths in .json",
    - 'mktasks': "Creates the tasks specified in the <user>.json, -o to override all in windows, -u to execute when logged into this user only",
    - 'shtasks': "Shows the created tasks",
    - 'rmtasks': "Removes all tasks created in the system by this program, -f to confirm all in windows",
    - 'update': "Updates the program with the new version available from github",
    - config: Opens the <user>.json file in the editor to modify. Tries to open 'VsCode' by default, else 'notepad' on Windows and 'nano' on Posix. -n to not try to open VsCode
    - reinstall: Reinstalls the program globally, aplying the new updates from 'kbase-git update'
    - uninstall: Uninstalls the program globally
If you put ['-g'], instead of moving or downloading the directory you are in, it will upload/download all the paths to keybase that you have put in the file '[username].json'

#### 'example.json':
```
{
    "tasks":{
        "lunch_break_upload": "15:15",
        "night_break_upload": "01:00"
    },
    "paths":[
        "C:\\example\\for\\windows\\path",
        "/example/for/posix/path",
        "~/another/posix/example"
    ]
}
```

## Add Task on computer
For MAC OS users!!
First you have to allow 'cron' and 'smbd' access to the disk for it to work -> https://osxdaily.com/2020/04/27/fix-cron-permissions-macos-full-disk-access/
- For the script to run automatically several times every day, you have to create a TASK on the computer that executes 'kbase-git -g -a'. To do this, enter the command 'kbase-git mktasks' (two default tasks will be created for you). If you want to change the hours or add tasks, enter 'kbase-git config' to modify the '/configs/[user].json' file that is created in the installation and retype 'kbase-git mktasks'. Make sure to put times when the computer is on and you are not using it to work on projects! Also save the changes in the files that you modify, because if the upload time comes and you have not done ctrl-s in any file, the changes may be lost.