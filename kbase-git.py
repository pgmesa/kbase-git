
import os
import sys
import json
from time import sleep
from pathlib import Path
from subprocess import Popen, run, PIPE

# --- User Variables
# -------------------------
# Change the user name to the one you use in keybase
username = 'pgmesa'
# Change the time the countdown will last (seconds)
counter = 15
# -------------------------

dir_ = Path(os.getcwd()).resolve()
execution_path = Path(__file__).resolve().parent

config_fname = 'config.json'
kbpath_to_upload = f'/keybase/private/{username}'

commands = {
    'upload': "Upload the added files of a git repository to keybase (including .git folder), --configured-paths",
    'download': "Downloads the previous files uploaded to the original git repository, --configured-paths",
}

def main():
    global counter
    print("----------- KeyBase-git Uploader -----------")
    print("--------------------------------------------")
    print(f" -> Cwd: '{dir_}'")
    print(f" -> Keybase username chosen: '{username}'")
    args = sys.argv; args.pop(0)
    if len(args) > 0:
        command = args[0]
        paths = [dir_]
        if command == 'upload' or command == 'download':
            if "--configured-paths" in args: 
                paths:list = get_config()['paths']
                if len(paths) == 0:
                    print("[!] No paths configured to upload/download")
                    return
                print("[%] Configured paths:")
                for path in paths: print(f" -> {path}")
                if command == 'upload':
                    print(f"[!] Countdown activated, your configured paths will be uploaded to keybase in {counter} seconds, press ctrl-c to cancel")
                    print(f"[%] -> ", end="", flush=True)
                    while counter > 0:
                        print(f" {counter}", end="", flush=True)
                        sleep(1)
                        counter -= 1
                    print() # Blank space
            if command == 'upload':
                upload(paths=paths)
            elif command == 'download':
                download(paths=paths)
        else:
            print(f"[!] '{command}' is not a valid command!") 
            print_help()
    else: print_help()
    print("--------------------------------------------")

# ---------- Utils ----------------
def get_config() -> dict:
    with open(execution_path/config_fname, 'rb') as file:
        config = json.load(file)
        return config

def process_git_stdout(out:str) -> list:
    return list(filter(lambda path: path != "", out.split('\n')))
        
def print_help():
    print("[?] Commands:")
    for command, info in commands.items():
        print(f"     - {command}: {info}")

# ------------ Commands --------------
def upload(paths:list):
    print("[%] Uploading paths...")  
    for path in paths:
        if type(path) != Path:
            path = Path(path).resolve()
        if not os.path.exists(path):
            print(f"[!] '{path}' doesn't exist (ignoring)")
            continue
        print(f"[%] Uploading '{path}'...")
        process = run('git ls-files', shell=True, cwd=path, stdout=PIPE)
        if process.returncode != 0:
            print(" -> [!] Upload failed, 'git ls-files' command failed (git not installed or not a git repo)")
            continue
        out = process.stdout.decode()[:-1]
        paths_to_upload:list = process_git_stdout(out)
        if len(paths_to_upload) == 0:
            print(" -> [!] This directory has no files added to git")
            continue
        # Eliminamos archivos y movemos el .git a keybase
        git_path = Path(path).resolve()
        keybase_path = kbpath_to_upload+"/"+git_path.name
        # Vemos is el nombre ya existe en keybase
        process = run(f'keybase fs ls {kbpath_to_upload}', shell=True, stdout=PIPE)
        out = process.stdout.decode()[:-1]
        kb_folders:list = process_git_stdout(out)
        if git_path.name in kb_folders:
            print(f" -> [!] '{git_path.name}' folder already exists in '{kbpath_to_upload}'")
            continue
        run(f'keybase fs mkdir {keybase_path}')
        process = run('git rm -rf .', shell=True, cwd=git_path, stdout=PIPE)
        if process.returncode != 0:
            print(" -> [!] Some errors appeared in the process")
        process = run('git commit -m "Keybase Upload"', shell=True, cwd=git_path, stdout=PIPE)
        move = run(f"keybase fs mv .git {keybase_path}", cwd=git_path)
        if move.returncode != 0:
            print(" -> [!] Could not move .git folder into keybase")      
        else:
            print(" -> [%] Folder uploaded successfully")
    
def download(paths:list):
    print("[%] Downloading paths...")  
    for path in paths:
        if type(path) != Path:
            path = Path(path).resolve()
        if not os.path.exists(path):
            print(f"[!] '{path}' doesn't exist (ignoring)")
            continue
        print(f"[%] Downloading '{path}'...")
        # Movemos el .git de keybase a su carpeta original y restauramos los archivos
        git_path = Path(path).resolve()
        keybase_path = kbpath_to_upload+"/"+git_path.name
        
        move = run(f"keybase fs mv {keybase_path+'/.git'} .", cwd=git_path, stderr=PIPE, stdout=PIPE)
        if move.returncode != 0:
            print(f" -> [!] Could not download .git folder, maybe '{git_path.name}' doesn't exist on keybase")
            continue
        else:
            run(f"keybase fs rm {keybase_path}")
        process = run('git reset --hard HEAD~1', shell=True, cwd=git_path, stdout=PIPE)
        if process.returncode != 0:
            print(" -> [!] Some errors appeared in the process")      
        else:
            print(" -> [%] Folder restored successfully")  

if "__main__" == __name__:
    try:
        print("[%] Program started (ctrl-c to exit)")
        main()
        print("[%] Program finished successfully")
    except KeyboardInterrupt:
        print("[!] Exit")
        exit(1)
    except Exception as err:
        print(f"[!] Unexpected Error: {err}")
        input("-> Press Enter to exit")
        exit(1)