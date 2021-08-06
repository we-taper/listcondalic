"""Use conda list and conda search to find packages' licenses

Not finished. WIP.
"""
import json
import shutil
import sys
from typing import List, Optional

from loguru import logger

from listcondalic.utils import run


def setup_conda():
    conda_exe = shutil.which('conda')
    logger.info(f'Found conda: {conda_exe}')
    if conda_exe is None:
        raise RuntimeError('Cannot find conda executable in the path!')
    return conda_exe


conda_exe = setup_conda()


def list_conda(env) -> List[dict]:
    """List conda packages. Skip pip packages"""
    logger.info('here')
    ret = run(f"{conda_exe} list -n {env} --no-pip --json")
    return json.loads(ret)


def conda_search(package: str, use_local=False, timeout=None) -> Optional[dict]:
    """Search conda for information about a package
    
    Returns None is conda search did not finish within a reasonable
    amoutn of time.
    """
    logger.info(f'Looking for {package}')
    if use_local:
        cmd = f"{conda_exe} search --info --json --use-local {package}"
    else:
        cmd = f"{conda_exe} search --info --json {package}"
    ret = run(cmd, raise_error=False, timeout=timeout)
    if isinstance(ret, int):
        logger.error(f"Failed to find package data for {package}")
        return
    return json.loads(ret)


def extract_pkgspec(list_output):
    return f"{list_output['name']}=={list_output['version']}"


def extract_license(conda_info: dict) -> dict:
    ret = {}
    for k, v in conda_info.items():
        license0 = None
        for oneresult in v:
            if license0 is None:
                license0 = oneresult.get('license', None)
            elif license0 != oneresult.get('license', None):
                raise RuntimeError(f'Different license found for {k}={v}')
        ret[k] = license0 if license0 is not None else 'N/A'
    return ret


def main(env_name, output):
    logger.remove()
    logger.add(sys.stderr, level='INFO')
    logger.info('here')
    pkg_lists = list(map(extract_pkgspec, list_conda(env_name)))
    print('Searching package data using conda search. May take a while.')
    logger.info('here')
    pkg_list = list(map(conda_search, pkg_lists))
    database = {}
    for pkg in pkg_list:
        database.update(extract_license(pkg))
    with open(output, 'w') as f:
        json.dump(output, f, indent=2)
