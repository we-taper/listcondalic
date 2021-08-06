from listcondalic.liccheck_and_condameta_based import main as _main
import click
from listcondalic import _version
__version__ = _version.get_versions()['version']

_help = """\
KIND: Either conda or pip.
FILE: the dependency file.
"""
@click.command("List licenses and versions", help=_help)
@click.argument('kind')
@click.argument('file')
@click.option('--restrict', is_flag=True, help='If true, will restrict the dependencies to those inside the conda yaml file.')
def main(kind, file, restrict):
    _main(kind=kind, file=file, restrict=restrict)
