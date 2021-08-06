import os
import re
import shutil
import subprocess
import time
from loguru import logger


def get_shell():
    for choice in ('zsh', 'powershell', 'bash'):
        if shutil.which(choice):
            return shutil.which(choice)
    raise RuntimeError("Cannot find a shell.")


shell_path = get_shell()



def run(cmd, raise_error=True, timeout=None) -> str:
    """Return result line by line.
    
    Returns -1 if the command failed but did not raise error."""
    logger.debug(f'Running {cmd}')
    t0 = time.time()
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, text=True,
        env=os.environ, shell=True, executable=shell_path
    )
    try:
        stdout, stderr = popen.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        popen.kill()
        stdout, stderr = popen.communicate()
        return -1
    t1 = time.time()
    logger.debug(f'Time cost: {t1 - t0}')
    return_code = popen.returncode
    if return_code != 0:
        if raise_error:
            raise ChildProcessError(f'Command finished with return code {return_code}: {cmd}')
        else:
            return -1
    del stderr  # ignore it
    ret = stdout
    # remove ansi escape string
    # Ref: https://stackoverflow.com/a/14693789/3383878
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', ret)

