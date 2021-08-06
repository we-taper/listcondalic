"""Use liccheck and conda-meta folder to get all licenses"""
import csv
import json
import os
import re
import sys
import tempfile
from os import path
from pprint import pprint
from typing import Dict, List

import pydantic
from yaml import Loader, load

from listcondalic.modified_liccheck import main as liccheck
from listcondalic.utils import run


class PkgInfo(pydantic.BaseModel):
    version: str
    license: str

NotFound = PkgInfo(version='NotFound', license='NotFound')

def list_conda_meta() -> Dict[str, PkgInfo]:
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
        keys = ('license', 'version')
        pkg = PkgInfo(**{k: content[k] for k in keys})
        pkgs[content['name']] = pkg
    return pkgs


def list_pip_packages_pip_license() -> Dict[str, PkgInfo]:
    items = json.loads(run('pip-licenses -f json'))
    res = {}
    for item in items:
        res[item['Name']] = PkgInfo(version=item['Version'], license=item['License'])
    return res

def list_pip_packages_requirements(requirement_file) -> Dict[str, PkgInfo]:
    with tempfile.TemporaryDirectory() as dir:
        setup = path.join(dir, 'setup.ini')
        with open(setup, 'w') as f:
            f.write('[Licenses]')
        cmd = f"-s {setup} -r {requirement_file} --level=Paranoid"
        packages = liccheck(cmd.split(' '))
    res = {}
    for idx in range(len(packages)):
        keys = ('version', 'license')
        res[packages[idx]['name']] = PkgInfo(**{k: packages[idx][k] for k in keys})
    return res


def read_conda_env_yml(yml_path) -> List[str]:
    with open(yml_path, 'r') as f:
        config = load(f, Loader=Loader)
    try:
        dependencies = config['dependencies']
    except KeyError:
        raise RuntimeError(
            f'Key dependencies not found in the yaml config {yml_path}')
    real_dep = []
    pattern = re.compile(r'[=>!~]')
    for item in dependencies:
        if isinstance(item, dict):
            # a pip dependency
            for _, v in item.items():
                real_dep.extend(v)
        else:
            item = str(item).replace(' ', '')
            if found := pattern.findall(item):
                # strip off all items after the first match of the pattern
                item = item[:item.find(found[0])]
            real_dep.append(item)
    dependencies = real_dep
    return dependencies


def main(kind: str, file: str, output=sys.stdout):
    database = {}
    if kind.lower() == 'conda':
        dependencies = read_conda_env_yml(file)
        installed = (list_pip_packages_pip_license(), list_conda_meta())
        pprint(installed[0])
        print('-' * 80)
        pprint(installed[1])

        for name in dependencies:
            if name in installed[0]:
                database[name] = installed[0][name]
            elif name in installed[1]:
                database[name] = installed[1][name]
            else:
                database[name] = NotFound
    elif kind.lower() == 'pip':
        database = list_pip_packages_requirements(file)
    else:
        raise ValueError(f'Only accept conda or pip as kind. It is {kind}')
    toprint = []
    for name, info in database.items():
        info = info.dict()
        info['name'] = name
        toprint.append(info)
    toprint = sorted(toprint, key=lambda k: k['name'])
    fieldnames = ('name', 'license', 'version')
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(toprint)


if __name__ == "__main__":
    main(kind='conda', file='/home/hx/code/listcondalic/test_example.yml')
