from listcondalic.liccheck_and_condameta_based import main as _main
import click

_help = """\
KIND: Either conda or pip.
FILE: the dependency file.
"""
@click.command("List licenses and versions", help=_help)
@click.argument('kind')
@click.argument('file')
@click.option('--all', is_flag=True, help='If true, will include all dependencies for conda-based yaml file.')
def main(kind, file, all):
    print('-' * 30 + ' OUTPUT CSV ' + '-' * 30)
    _main(kind=kind, file=file, all=all)
    print('-' * 30 + '    DONE    ' + '-' * 30)



if __name__ == "__main__":
    main()
