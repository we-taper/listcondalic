import sys
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
def main(kind, file):
    from loguru import logger
    logger.remove()
    logger.add(sys.stderr, level='INFO')
    _main(kind=kind, file=file)
