import os
import sys
import json
import platform
from pathlib import Path
from subprocess import run, PIPE

try:
    username = run('keybase whoami', shell=True, stdout=PIPE, check=True).stdout.decode().strip()
except:
    print("ERROR: You seem to be offline, not logged in to keybase or not in skin4loud keybase team")
    exit(1)
    
mark = "#PATH#"
system = platform.system()
extension = ".bat" if system == "Windows" else ".sh"
folder = "win" if system == "Windows" else "posix"
target_file = 'kbase-git'+extension
kb_dest_dir = f'/keybase/team/skin4cloud/kbase-git_uploads/{username}'
execution_path = Path(__file__).resolve().parent
shell_fpath = execution_path/folder/target_file
main_path = execution_path.parent

def check():
    config_path = main_path/f'configs/{username}.json'
    if not os.path.exists(config_path):
        with open(config_path, 'w') as file:
            json.dump({"paths":[]}, file, indent=4)
    run(f"keybase fs mkdir {kb_dest_dir}")

def do(action=None):
    with open(shell_fpath, 'r') as file:
        content = file.read()
    with open(shell_fpath, 'w') as file:
        if action == '--replace':
            file.write(content.replace(mark, str(main_path)))
        elif action == '--reset':
            file.write(content.replace(str(main_path), mark))

if __name__ == "__main__":
    args = sys.argv; args.pop(0)
    check()
    if len(args) > 0:
        action = args[0]
        if '--replace' == action:
            do(action=action)
        elif '--reset' == action:
            do(action=action)