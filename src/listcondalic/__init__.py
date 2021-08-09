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
@click.option('-v', '--verbose', count=True)
def main(kind, file, verbose):
    assert verbose >= 0
    if verbose == 0:
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level='ERROR')
    elif verbose == 1:
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level="DEBUG")
    elif verbose > 1:
        from loguru import logger
        logger.remove()
        logger.add(sys.stderr, level="TRACE")

    _main(kind=kind, file=file)
