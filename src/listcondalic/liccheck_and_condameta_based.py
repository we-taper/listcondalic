"""Use liccheck and conda-meta folder to get all licenses"""
from io import StringIO
import json
import os
import re
import sys
import tempfile
from os import path
from typing import Dict, List

from yaml import Loader, load

from listcondalic.modified_liccheck import main as liccheck
from loguru import logger

_NotFound = 'NotFound'


def list_conda_meta(retain: tuple = None) -> Dict[str, dict]:
    try:
        conda_dir = os.environ['CONDA_PREFIX']
    except KeyError:
        raise RuntimeError(
            "Cannot access CONDA_PREFIX environment variable. Please check"
            "if conda has been properly initiated.")
    meta = path.join(conda_dir, 'conda-meta')
    pkgs = {}
    for file in os.listdir(meta):
        if not file.endswith('json'):
            continue
        with open(path.join(meta, file)) as f:
            content = json.load(f)
        pkgs[content['name']] = {
            k: v
            for k, v in content.items() if retain is None or k in retain
        }
    return pkgs


def list_pip_packages_requirements(requirement_file) -> Dict[str, str]:
    with tempfile.TemporaryDirectory() as dir:
        setup = path.join(dir, 'setup.ini')
        with open(setup, 'w') as f:
            f.write('[Licenses]')
        cmd = f"-s {setup} -r {requirement_file} --level=Paranoid"
        from contextlib import redirect_stdout
        with redirect_stdout(StringIO()):  # throw away its rubbish output
            packages = liccheck(cmd.split(' '))
    res = {}
    for idx in range(len(packages)):
        res[packages[idx]['name']] = packages[idx]['license']
    return res


_pattern = re.compile(r'\s*[=><!~].*')


def strip_version_info(name: str):
    logger.trace(f'strip_version_info:name:{name}')
    found = _pattern.findall(name)
    if found:
        # strip off all items after the first match of the pattern
        name = name[:name.find(found[0])]
    logger.trace(f"strip_version_info:outname:{name}")
    return name


def read_conda_env_yml(yml_path) -> List[str]:
    with open(yml_path, 'r') as f:
        data = load(f, Loader=Loader)
    pip = set()
    conda = set()
    for item in data['dependencies']:
        if isinstance(item, dict):
            if 'pip' in item:
                pip.update(item['pip'])
        else:
            conda.add(str(item))
    return conda, pip


PACKAGES_TO_IGNORE = {'python', 'setuptools', 'wheel', 'pip'}
PACKAGES_TO_IGNORE_REGEX = {re.compile(r'python_abi.*')}


def should_ignore(name):
    if name in PACKAGES_TO_IGNORE:
        return True
    for p in PACKAGES_TO_IGNORE_REGEX:
        if p.match(name):
            return True
    return False


def do_conda(yml_file):
    conda_part, pip_part = read_conda_env_yml(yml_file)
    logger.debug(f'conda_part=\n{conda_part}')
    logger.debug(f'pip_part=\n{pip_part}')
    from pathlib import Path
    with tempfile.TemporaryDirectory() as folder:
        folder = Path(folder)
        reqfile = folder / 'req.txt'
        reqfile.write_text('\n'.join(pip_part))
        conda_pip_part_lic = list_pip_packages_requirements(reqfile.absolute())

    conda_pip_part_lic = {
        k: v
        for k, v in conda_pip_part_lic.items() if not should_ignore(k)
    }
    logger.debug(f'conda_pip_part_lic=\n{conda_pip_part_lic}')

    conda_metadata = list_conda_meta(retain=('license', 'depends'))

    def explore_depthfirst(parent, visited: set):
        parent = strip_version_info(parent)
        visited.add(parent)
        parent = conda_metadata.get(parent, None)
        if parent:
            children = parent.get('depends', [])
            children = list(map(strip_version_info, children))
            visited.update(children)
            for child in children:
                if child not in visited:
                    explore_depthfirst(child, visited)

    conda_part_added_dependency = set()
    for item in conda_part:
        explore_depthfirst(item, conda_part_added_dependency)
    logger.debug(f'conda_part_added_dependency\n{conda_part_added_dependency}')

    def get_licence_conda_meta(k):
        if k in conda_metadata:
            return conda_metadata[k].get('license', _NotFound)
        return _NotFound

    conda_conda_part_lic = {
        k: get_licence_conda_meta(k)
        for k in conda_part_added_dependency if not should_ignore(k)
    }
    logger.debug(f'conda_conda_part_lic=\n{conda_conda_part_lic}')
    total = conda_pip_part_lic.copy()
    total.update(conda_conda_part_lic)
    return total


def main(kind: str, file: str, output=sys.stdout):
    database = {}
    if kind.lower() == 'conda':
        database = do_conda(file)
    elif kind.lower() == 'pip':
        database = list_pip_packages_requirements(file)
    else:
        raise ValueError(f'Only accept conda or pip as kind. It is {kind}')
    json.dump(database, output, indent=2)
