
import os
import sys
import json
import platform
import traceback
from time import sleep
from pathlib import Path
from subprocess import CalledProcessError, Popen, run, PIPE

import tasks
import kb_logging as logging

# -- Python version check ---
dig1, dig2 = sys.version.split('.')[:2]
require_d1, require_d2 = 3, 7
if require_d1 > int(dig1) or require_d2 > int(dig2):
    print("[!] ERROR: The python version must be 3.7 or higher")
    exit(1)
# ---------------------------

OS = platform.system()

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
    'upload': "Uploads the .git folder to keybase and removes the project locally, -g for configured paths in .json",
    'download': "Downloads the .git folder from keybase and restores the project, -g for configured paths in .json",
    'mktasks': "Creates the tasks specified in the <user>.json, -o to override all in windows",
    'shtasks': "Shows the created tasks",
    'rmtasks': "Removes all tasks created in the system by this program, -f to confirm all in windows",
}

print("Initializing program...")
# -- Global logger config
title = f"{username}"; title_end = ""
try:
    if sys.argv[1] in commands:
        title_end += "_"+sys.argv[1]
except: pass
if '-a' in sys.argv:
    title_end += "_auto"
logs_dir = kbpath_to_upload+f"/__logs__"
run(f'keybase fs mkdir {logs_dir}', shell=True)
logging.config_log_capture(logs_dir, logfile_title=title, title_end=title_end)
logging.root_level = logging.DEBUG
logging.start_log_capture()
# -- Logger
logger = logging.Logger(module_name=__name__, show_fname=False)
logger.level = logging.DEBUG

DEBUG = True
counter_flag = False

def main():
    global counter_flag
    logger.info(f"System: '{OS}'")
    logger.info(f"Cwd: '{dir_}'")
    logger.info(f"Execution Path: {execution_path}")
    logger.info(f"Keybase username: '{username}'")
    if DEBUG:
        logger.info(f"DEBUG Mode Activated")
    args = sys.argv; args.pop(0)
    logger.info(f"args => {args}", sysout=False)
    try:
        config = get_config()
    except Exception as err:
        logger.error(f"Configuration failed '{username}.json': \n{err}")
        return
    if "-h" in args:
        print_help()
    if len(args) > 0:
        command = args[0]
        paths = [dir_]
        if command == 'upload' or command == 'download':
            if "--counter" in args:
                counter_flag = True
            if "-g" in args: 
                paths:list = config['paths']
                if len(paths) == 0:
                    logger.error("No paths configured to upload/download")
                    return
                logger.info("Configured paths:")
                for path in paths: logger.info(f" -> {path}")
                if command == 'upload':
                    for path in paths:
                        if not check_name(Path(path).name):
                            break
                    else:
                        logger.info("Everything seems already uploaded")
                        return
                    if counter_flag:
                        msg1 = f"your configured paths will be uploaded to keybase in {counter} seconds"
                        logger.info(f"Countdown activated, {msg1} (press ctrl-c to cancel)")
                        init_counter(counter)
            if command == 'upload':
                upload(paths=paths)
            elif command == 'download':
                download(paths=paths)
        elif command == 'mktasks':
            override = False
            if '-o' in args:
                override = True
            configured_tasks = config["tasks"]
            tasks.create_task(OS, configured_tasks, override=override)
        elif command == 'shtasks':
            tasks.show_tasks(OS=OS)
        elif command == 'rmtasks':  
            force = False
            if '-f' in args:
                force = True 
            tasks.remove_tasks(OS=OS, force=force)
        else:
            logger.error(f"'{command}' is not a valid command!") 
            print_help()
    else: 
        print_help()

# ---------- Utils ----------------
def login_intent(show_msg:bool=True) -> bool:
    if show_msg:
        print("[%] Iniciando sesión en keybase (ctrl-c para reintentar si se queda pillado)...")
        print("[%] Puede ser necesario tener que reintentar un par de veces")    
        print("[%] En ocasiones el cuadro no se muestra en pantalla pero esta abierto en la barra de tareas")
        print("[%] En caso de que no salga un cuadro de input, reintentar comando o iniciar sesion desde la app de keybase")
    try:
        Popen('keybase login', check=True, shell=True).wait()
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
    logger.log("Printing Help", sysout=False)
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
    logger.info("Uploading paths...")  
    for path in paths:
        if type(path) != Path:
            path = Path(path).resolve()
        if not os.path.exists(path):
            logger.error(f"'{path}' doesn't exist (ignoring)")
            continue
        logger.info(f"Uploading '{path}'...")
        cmd = 'git ls-files'; logger.log(cmd, sysout=False)
        process = run(cmd, shell=True, cwd=path, stdout=PIPE)
        if process.returncode != 0:
            logger.error("Upload failed, 'git ls-files' command failed (git not installed or not a git repo)")
            continue
        out = process.stdout.decode()
        paths_to_upload:list = process_listed_stdout(out)
        if len(paths_to_upload) == 0:
            logger.error("This directory has no files added to git")
            continue
        # Eliminamos archivos y movemos el .git a keybase
        git_path = Path(path).resolve()
        keybase_path = kbpath_to_upload+"/"+git_path.name
        # Vemos si el nombre ya existe en keybase
        if check_name(git_path.name):
            logger.error(f"'{git_path.name}' folder already exists in '{kbpath_to_upload}'")
            continue
        run(f'keybase fs mkdir {keybase_path}', shell=True)
        cmd = 'git rm -rf .'; logger.log(cmd, sysout=False)
        process = run(cmd, shell=True, cwd=git_path, stdout=PIPE)
        if process.returncode != 0:
            logger.error("Some errors appeared in the process")
        cmd = 'git commit -m "Keybase Upload"'; logger.log(cmd, sysout=False)
        run(cmd, shell=True, cwd=git_path, stdout=PIPE)
        cmd = f"keybase fs mv .git {keybase_path}"; logger.log(cmd, sysout=False)
        move = run(cmd, cwd=git_path, shell=True)
        if move.returncode != 0:
            logger.error("Could not move .git folder into keybase")      
        else:
            logger.info("Folder uploaded successfully")
    
def download(paths:list):
    logger.info("Downloading paths...")  
    for path in paths:
        if type(path) != Path:
            path = Path(path).resolve()
        if not os.path.exists(path):
            logger.error(f"'{path}' doesn't exist (ignoring)")
            continue
        logger.info(f"Downloading '{path}'...")
        # Movemos el .git de keybase a su carpeta original y restauramos los archivos
        git_path = Path(path).resolve()
        keybase_path = kbpath_to_upload+"/"+git_path.name
        cmd =f"keybase fs mv {keybase_path+'/.git'} ."; logger.log(cmd, sysout=False)
        move = run(cmd, cwd=git_path, stderr=PIPE, stdout=PIPE, shell=True)
        if move.returncode != 0:
            logger.error(f"Could not download .git folder, maybe '{git_path.name}' doesn't exist on keybase")
            continue
        else:
            cmd = f"keybase fs rm {keybase_path}"; logger.log(cmd, sysout=False)
            run(cmd, shell=True)
        cmd ='git reset --hard HEAD~1'; logger.log(cmd, sysout=False)
        process = run(cmd, shell=True, cwd=git_path, stdout=PIPE)
        if process.returncode != 0:
            logger.error("Some errors appeared in the process")      
        else:
            logger.info("Folder restored successfully")  

if "__main__" == __name__:
    error = False
    try:
        print("[%] Program started (ctrl-c to exit)")
        print("----------- KeyBase-git Uploader -----------")
        print("--------------------------------------------")
        main()
        print("--------------------------------------------")
    except KeyboardInterrupt:
        logger.warning("Exit (ctrl-c)")
        error = True
    except Exception as err:
        sysout = False
        if DEBUG: sysout = True
        logger.critical(traceback.format_exc(), sysout=sysout)
        if not DEBUG:
            logger.critical(f"Unexpected Error: {err}")
        error = True
    finally:
        logging.flush()
    if counter_flag:
        print(f"[%] Program will exit in {time_to_exit} seconds:")
        init_counter(time_to_exit)
    if error: 
        input("-> Press Enter to exit")
        exit(1)