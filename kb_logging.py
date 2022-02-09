
import os
import calendar
import datetime as dt
from pathlib import Path
from subprocess import run, PIPE

DEBUG = 0
INFO = 10
WARNING = 20
ERROR = 30
CRITICAL = 40

root_level = DEBUG
capture_logs = False

_logs_dir = None
_log_fname = None
_log_file_path = None
execution_path = Path(__file__).resolve().parent

def config_log_capture(logsdir:str, logfile_title:str='', title_end:str='', start=True):
    global _logs_dir, _log_fname, _log_file_path
    _logs_dir = create_kb_path(logsdir)
    _log_fname = _generate_logfname(logfile_title)+title_end 
    _log_file_path = _logs_dir+"/"+_log_fname
    if start: start_log_capture()
    
def create_kb_path(logsdir:str) -> str:
    date = dt.datetime.today()
    run(f'keybase fs mkdir {logsdir}', shell=True)
    year = date.year; logsdir += f'/{year}'
    run(f'keybase fs mkdir {logsdir}', shell=True)
    month = calendar.month_name[date.month]; logsdir += f'/{month}'
    run(f'keybase fs mkdir {logsdir}', shell=True)
    day = date.day; logsdir += f'/{day}'
    run(f'keybase fs mkdir {logsdir}', shell=True)
    return logsdir
 
def start_log_capture():
    global capture_logs
    capture_logs = True
    
def stop_log_capture():
    global capture_logs
    capture_logs = False
    
def flush():
    run(f'keybase fs mv ./{_log_fname} {_log_file_path}', cwd=execution_path, shell=True, stdout=PIPE)
    if os.path.exists(execution_path/_log_fname):
        os.remove(execution_path/_log_fname)
    
def _generate_logfname(title:str) -> str:
    date = _get_date(path_friendly=True)
    return title + "_" + date

def _get_date(path_friendly:bool=False) -> str:
    datetime = dt.datetime.now()
    if path_friendly:
        date = str(datetime.date())
        time = str(datetime.time()).replace(':', "-").replace('.', '_')
        return date+"_"+time
    else:
        return str(datetime)
    
# -------------------------------------------------------------------
class LogError(Exception):
    pass

class Logger():
    
    capture_logs = True
    
    def __init__(self, module_name:str=None, level=DEBUG, sysout:bool=True, show_fname:bool=False) -> None:
        self.module_name = module_name
        self.level = level
        self.sysout = sysout
        self.show_fname = show_fname
        
    def capture_logs(self):
        self.capture_logs = True
    
    def free_logs(self):
        self.capture_logs = False
     
    def debug(self, msg:str, nl:bool=False, sysout:bool=True):
        _level = DEBUG; symbol = '[DEBUG]'
        if self._check_level(_level):
            self._process(msg, symbol=symbol, nl=nl, sysout=sysout)
    
    def info(self, msg:str,nl:bool=False, sysout:bool=True):
        _level = INFO; symbol = '[INFO]'
        if self._check_level(_level):
            self._process(msg, symbol=symbol, nl=nl, sysout=sysout)
    
    def warning(self, msg:str, nl:bool=False, sysout:bool=True):
        _level = WARNING; symbol = '[WARNING]'
        if self._check_level(_level):
            self._process(msg, symbol=symbol, nl=nl, sysout=sysout)  
        
    def error(self, msg:str, nl:bool=False, sysout:bool=True):
        _level = ERROR; symbol = '[ERROR]'
        if self._check_level(_level):
            self._process(msg, symbol=symbol, nl=nl, sysout=sysout)
    
    def critical(self, msg:str, nl:bool=False, sysout:bool=True):
        _level = CRITICAL; symbol = '[CRITICAl]'
        if self._check_level(_level):
            self._process(msg, symbol=symbol, nl=nl, sysout=sysout)
    
    def log(self, msg:str, nl:bool=False, sysout:bool=True):
        symbol = '[LOG]'
        self._process(msg, symbol=symbol, nl=nl, sysout=sysout)
            
    def _check_level(self, level:int):
        if not root_level > level and not self.level > level:
            return True
        return False
    
    def _process(self, msg:str, symbol:str='', nl:bool=False, sysout:bool=True):
        log = self._get_log(msg, symbol=symbol, nl=nl)
        self._capture(log)
        if sysout:
            log = self._get_log(msg, symbol=symbol, nl=nl, showfn=self.show_fname)
            self._print(log)
    
    def _get_log(self, msg:str, symbol:str='', nl:bool=False, showfn=True) -> str:
        log = symbol+" "
        if self.module_name is not None and showfn:
            log += self.module_name+": "
        log += str(msg)
        if nl: log = "\n"+log
        
        return log
    
    def _capture(self, log:str):
        if not capture_logs or not self.capture_logs: return
        log_date = _get_date()
        with open(execution_path/_log_fname, 'ab') as file:
            if log.startswith('\n'):
                log = log[1:]
            final_log = "\n\n"+log_date+"\n"+log
            file.write(final_log.encode('utf-8'))
    
    def _print(self, log:str):
        if not self.sysout: return
        print(log)
        