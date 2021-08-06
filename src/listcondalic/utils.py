import os
import re
import shutil
import subprocess



def get_shell():
    for choice in ('zsh', 'powershell', 'bash'):
        if shutil.which(choice):
            return shutil.which(choice)
    raise RuntimeError("Cannot find a shell.")


shell_path = get_shell()



def run(cmd, failure_ok=False) -> str:
    """Return result line by line."""
    popen = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, text=True,
        env=os.environ, shell=True, executable=shell_path
    )
    return_code = popen.wait()
    if return_code != 0 and not failure_ok:
        raise ChildProcessError(f'Command finished with return code {return_code}: {cmd}')
    ret = ''.join(popen.stdout.readlines())
    # remove ansi escape string
    # Ref: https://stackoverflow.com/a/14693789/3383878
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', ret)

