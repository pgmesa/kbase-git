
import os
import csv
import kb_logging as logging
from pathlib import Path
from subprocess import CalledProcessError, Popen, run, PIPE

win_tasks_dir = "KbaseGitTasks"
task_command = "kbase-git upload -g -a"
execution_path = Path(__file__).resolve().parent
# -- Logger
logger = logging.Logger(module_name=__name__, show_fname=False)
logger.level = logging.DEBUG

def create_task(OS:str, tasks:dict, override=False, current_user:bool=False):
    if override:
        remove_tasks(OS, force=True)
    if OS == "Windows":
        for task_name, time in tasks.items():
            try:
                check_input_time(time)
            except Exception as err:
                msg = (f"El tiempo introducido '{time}' no es correcto" + 
                        f"\n     ERR MSG -> {err}")
                logger.error(msg)
                continue
            np = "" if current_user else "/NP"
            cmd = (f'SCHTASKS /CREATE /SC DAILY /TN "{win_tasks_dir}\\{task_name}" ' +
                    f'/TR "{task_command}" /ST {time} {np}') 
            logger.log(cmd, sysout=False)
            logger.info(f"Creating '{task_name}' at '{time}'")
            p = Popen(cmd, shell=True, stderr=PIPE)
            p.wait()
            if p.returncode != 0:
                logger.warning("Operation Cancelled", sysout=False)
            else:
                logger.info("Task created successfully", sysout=False)
    else:
        # Comprobamos si cron esta corriendo
        out = run('service cron status', shell=True, stdout=PIPE).stdout.decode()
        if "cron is not running" in out:
            logger.info("(sudo) Activando servicio de cron para crear tareas...")
            cmd = 'sudo service cron start'; logger.log(cmd, sysout=False)
            p = Popen(cmd, shell=True, stdout=PIPE)
            p.wait()
            if p.returncode != 0:
                logger.error("No se pudo iniciar 'cron deamon'")
                return
        # Comprobamos si los logs del sistema estan activados
        out = run('service rsyslog status', shell=True, stdout=PIPE).stdout.decode()
        if "rsyslogd is not running" in out:
            logger.info("(sudo) Activando servicio de logs del sistema...")
            cmd = 'sudo service rsyslog start'; logger.log(cmd, sysout=False)
            p = Popen(cmd, shell=True, stdout=PIPE)
            p.wait()
            if p.returncode != 0:
                logger.error("No se pudo iniciar 'rsyslog deamon'")
                return
        extasks = get_tasks(OS)
        if len(extasks) != 0:
            show_tasks(OS)
            answer = str(input("WARNING: There are already tasks scheduled on crontab. Override? (y/n): "))
            if answer.lower() != 'y':
                logger.warning("Operation Cancelled")
                return
        cronfile = "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\n"
        for task_name, time in tasks.items():
            try:
                check_input_time(time)
            except Exception as err:
                msg = (f" El tiempo introducido '{time}' no es correcto" + 
                        f"\n     ERR MSG -> {err}")
                logger.error(msg)
                continue
            hours = int(time[:2]); mins = int(time[3:])
            cron_task = f"{mins} {hours} * * * {task_command}"
            cronfile += f"# {task_name}\n{cron_task}\n"
            logger.info(f"Adding '{task_name}': '{cron_task}'")
        if cronfile != "":
            cron_fpath = execution_path/'tempsh'
            with open(cron_fpath, 'w') as file:
                file.write(cronfile)
            cmd = f'crontab "{cron_fpath}"'; logger.log(cmd, sysout=False)
            p = run(cmd, shell=True)
            if p.returncode == 0:
                logger.info("Tasks created successfully")
            else:
                logger.error("Error while saving tasks in crontab")
            os.remove(cron_fpath)
        
def show_tasks(OS:str):
    logger.info(" + Scheduled Tasks:")
    tasks = get_tasks(OS)
    if len(tasks) == 0:
        logger.info("No tasks scheduled")
        return
    if OS == "Windows":
        cmd = f'schtasks /query /fo TABLE /tn "{win_tasks_dir}\\\\"'
        logger.log(cmd, sysout=False)
        out = run(cmd, shell=True, check=True, stderr=PIPE, stdout=PIPE).stdout.decode()[:-2]
        logger.log(out)
    else:
        for task in tasks: 
            logger.log("     -> " + task)
    
def remove_tasks(OS:str, force=False):
    tasks = get_tasks(OS)
    if len(tasks) == 0:
        logger.info("No tasks to remove")
        return
    f = ""
    if force: f = "/F"
    show_tasks(OS)
    if OS == "Windows":
        for task in tasks:
            logger.info(f"Deleting '{task}'...")
            cmd = (f'SCHTASKS /DELETE /TN "{task}" {f}')
            logger.log(cmd, sysout=False)
            p = Popen(cmd, shell=True); p.wait()
            extasks = get_tasks(OS)
            if task in extasks:
                logger.warning("Operation Cancelled",sysout=False)
            else:
                logger.info("Task deleted successfully",sysout=False)
    else:
        cmd = 'crontab -r'
        logger.log(cmd, sysout=False)
        p = run(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        if p.returncode == 0:
            logger.info("Tasks removed successfully")
        else:
            logger.error("Error while removing crontab-file")
        
def get_tasks(OS:str) -> list:
    tasks = []
    if OS == 'Windows':
        cmd = f'schtasks /query /fo CSV /tn "{win_tasks_dir}\\\\"'
        str_csv = run(cmd, shell=True, stdout=PIPE, stderr=PIPE).stdout.decode()
        reader = csv.reader(str_csv.splitlines(), delimiter=',')
        for i, row in enumerate(reader):
            if i == 0: continue
            tasks.append(row[0])
    else:
        try:
            lines = run('crontab -l', shell=True, stdout=PIPE, stderr=PIPE).stdout.decode().splitlines()
        except CalledProcessError:
            pass
        else:
            tasks = list(filter(lambda line: "#" not in line and line != "" and "PATH=" not in line, lines))
    
    return tasks
        
def check_input_time(time:str) -> None:
    """Raises Exception if the format is not valid"""
    if len(time) == 5 and time[2] == ":":
        try:
            hour = int(time[:2])
            minutes = int(time[3:])
        except:
            msg = "wrong format (HH:MM) or some character is not a number"
            raise Exception(msg)
        else:
            cond1 = hour >= 0 and hour <= 23
            cond2 = minutes >= 0 and minutes <= 59
            if cond1:
                if cond2:
                    return
                else:
                    msg = ("minutes need to be between 0 and 59 " + 
                        f"-> '{minutes}' introduced")
                    raise Exception(msg)
            else:
                msg = ("hours need to be between 0 and 23 " + 
                        f"-> '{hour}' introduced")
                raise Exception(msg)             
    else:
        msg = "wrong format -> (HH:MM), example: 11:50"
        raise Exception(msg)