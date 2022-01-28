
import csv
from subprocess import CalledProcessError, Popen, run, PIPE

win_tasks_dir = "KbaseGitTasks"
task_command = "kbase-git upload -g --counter"

def create_task(OS:str, tasks:dict, override=False):
    if override:
        remove_tasks(OS, force=True)
    if OS == "Windows":
        for task_name, time in tasks.items():
            try:
                check_input_time(time)
            except Exception as err:
                msg = (f" El tiempo introducido '{time}' no es correcto" + 
                        f"\n     ERR MSG -> {err}")
                print(msg)
                continue
            cmd = (f'SCHTASKS /CREATE /SC DAILY /TN "{win_tasks_dir}\\{task_name}" ' +
                    f'/TR "{task_command}" /ST {time}')
            Popen(cmd, shell=True).wait()
    else:
        ...
    
def show_tasks(OS:str):
    print(" + Scheduled Tasks:")
    tasks = get_tasks(OS)
    if len(tasks) == 0:
        print(" [%] No tasks scheduled")
        return
    if OS == "Windows":
        cmd = f"schtasks /query /fo TABLE /tn {win_tasks_dir}\\"
        run(cmd, shell=True, check=True, stderr=PIPE)
    else:
        for task in tasks: print("     ->", task)
    
def remove_tasks(OS:str, force=False):
    tasks = get_tasks(OS)
    if len(tasks) == 0:
        print(" [%] No tasks to remove")
        return
    f = ""
    if force: f = "/F"
    if OS == "Windows":
        for task in tasks:
            cmd = (f'SCHTASKS /DELETE /TN "{task}" {f}')
            Popen(cmd, shell=True).wait()
    else:
        run('crontab -r', shell=True)
        print("[%] Tasks removed")
        
def get_tasks(OS:str) -> list:
    tasks = []
    if OS == 'Windows':
        cmd = f"schtasks /query /fo CSV /tn {win_tasks_dir}\\"
        str_csv = run(cmd, shell=True, stdout=PIPE, stderr=PIPE).stdout.decode()
        reader = csv.reader(str_csv.splitlines(), delimiter=',')
        for i, row in enumerate(reader):
            if i == 0: continue
            tasks.append(row[0])
    else:
        lines = run('crontab -l', shell=True, stdout=PIPE).stdout.decode().splitlines()
        tasks = list(filter(lambda line: "#" not in line and line != "", lines))
    
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