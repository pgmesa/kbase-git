
import os
import sys
import json
from time import sleep
from pathlib import Path
from subprocess import CalledProcessError, Popen, run, PIPE

# -- Python version check ---
dig1, dig2 = sys.version.split('.')[:2]
require_d1, require_d2 = 3, 7
if require_d1 > int(dig1) or require_d2 > int(dig2):
    print("[!] ERROR: The python version must be 3.7 or higher")
    exit(1)
# ---------------------------

try:
    username = run("keybase whoami", shell=True, stdout=PIPE, check=True).stdout.decode().strip()
except:
    print("[!] Error trying to get keybase username (keybase installed and logged in?)")
    exit(1)
    
kbpath_to_upload = f"/keybase/team/skin4cloud/kbase-git_uploads/{username}"

# Time the countdown will last (seconds)
counter = 10
time_to_exit = 5 

dir_ = Path(os.getcwd()).resolve()
execution_path = Path(__file__).resolve().parent

config_dir = execution_path/'configs'
config_example = 'example.json'
config_fpath = config_dir/f'{username}.json'

commands = {
    'upload': "Upload the added files of a git repository to keybase (including .git folder), --config-paths",
    'download': "Downloads the previous files uploaded to the original git repository, --config-paths",
    '--set-tasks': "Creates the tasks specified in the <user>.json",
    '--show-tasks': "Shows the created tasks",
    '--rm-tasks': "Removes all tasks created by this program"  
}

counter_flag = False

def main():
    global counter_flag
    print(f" -> Cwd: '{dir_}'")
    print(f" -> Keybase username: '{username}'")
    args = sys.argv; args.pop(0)
    if len(args) > 0:
        command = args[0]
        paths = [dir_]
        if command == 'upload' or command == 'download':
            if "--counter" in args:
                counter_flag = True
            if "--config-paths" in args: 
                paths:list = get_config()['paths']
                if len(paths) == 0:
                    print("[!] No paths configured to upload/download")
                    return
                print("[%] Configured paths:")
                for path in paths: print(f" -> {path}")
                if command == 'upload':
                    for path in paths:
                        if not check_name(Path(path).name):
                            break
                    else:
                        print("[%] Everything seems already uploaded")
                        return
                    if counter_flag:
                        msg1 = f"your configured paths will be uploaded to keybase in {counter} seconds"
                        print(f"[!] Countdown activated, {msg1} (press ctrl-c to cancel)")
                        init_counter(counter)
            if command == 'upload':
                upload(paths=paths)
            elif command == 'download':
                download(paths=paths)
        else:
            print(f"[!] '{command}' is not a valid command!") 
            print_help()
    else: print_help()

# ---------- Utils ----------------
def login_intent(show_msg:bool=True) -> bool:
    if show_msg:
        print("[%] Iniciando sesión en keybase (ctrl-c para reintentar si se queda pillado)...")
        print("[%] Puede ser necesario tener que reintentar un par de veces")    
        print("[%] En ocasiones el cuadro no se muestra en pantalla pero esta abierto en la barra de tareas")
        print("[%] En caso de que no salga un cuadro de input, reintentar comando o iniciar sesion desde la app de keybase")
    try:
        run('keybase login', check=True, shell=True)
    except CalledProcessError:
        return False
    except KeyboardInterrupt:
        answer = str(input("[%] Reintentar login? (y/n): "))
        if answer.lower() == "y":
            return login_intent(show_msg=False)
        return False
    return True
    
def get_config() -> dict:
    with open(config_fpath, 'rb') as file:
        config = json.load(file)
        return config

def process_listed_stdout(out:str) -> list:
    return list(filter(lambda path: path != "", out.split('\n')))
        
def print_help():
    print("[?] Commands:")
    for command, info in commands.items():
        print(f"     - {command}: {info}")

def check_name(dirname:str) -> bool:
    process = run(f'keybase fs ls {kbpath_to_upload} --one', shell=True, stdout=PIPE)
    out = process.stdout.decode()
    kb_folders:list = process_listed_stdout(out)
    if dirname in kb_folders:
        return True
    return False

def init_counter(seconds:int):
    t = seconds
    print(f"[%] -> ", end="", flush=True)
    while t > 0:
        print(f" {t}", end="", flush=True)
        sleep(1)
        t -= 1
    print() # Blank space

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
        out = process.stdout.decode()
        paths_to_upload:list = process_listed_stdout(out)
        if len(paths_to_upload) == 0:
            print(" -> [!] This directory has no files added to git")
            continue
        # Eliminamos archivos y movemos el .git a keybase
        git_path = Path(path).resolve()
        keybase_path = kbpath_to_upload+"/"+git_path.name
        # Vemos si el nombre ya existe en keybase
        if check_name(git_path.name):
            print(f" -> [!] '{git_path.name}' folder already exists in '{kbpath_to_upload}'")
            continue
        run(f'keybase fs mkdir {keybase_path}', shell=True)
        process = run('git rm -rf .', shell=True, cwd=git_path, stdout=PIPE)
        if process.returncode != 0:
            print(" -> [!] Some errors appeared in the process")
        process = run('git commit -m "Keybase Upload"', shell=True, cwd=git_path, stdout=PIPE)
        move = run(f"keybase fs mv .git {keybase_path}", cwd=git_path, shell=True)
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
        
        move = run(f"keybase fs mv {keybase_path+'/.git'} .", cwd=git_path, stderr=PIPE, stdout=PIPE, shell=True)
        if move.returncode != 0:
            print(f" -> [!] Could not download .git folder, maybe '{git_path.name}' doesn't exist on keybase")
            continue
        else:
            run(f"keybase fs rm {keybase_path}", shell=True)
        process = run('git reset --hard HEAD~1', shell=True, cwd=git_path, stdout=PIPE)
        if process.returncode != 0:
            print(" -> [!] Some errors appeared in the process")      
        else:
            print(" -> [%] Folder restored successfully")  

if "__main__" == __name__:
    try:
        print("[%] Program started (ctrl-c to exit)")
        print("----------- KeyBase-git Uploader -----------")
        print("--------------------------------------------")
        main()
        print("--------------------------------------------")
    except KeyboardInterrupt:
        print("[!] Exit")
        exit(1)
    except Exception as err:
        print(f"[!] Unexpected Error: {err}")
        input("-> Press Enter to exit")
        exit(1)
    if counter_flag:
        print(f"[%] Program will exit in {time_to_exit} seconds:")
        init_counter(time_to_exit)