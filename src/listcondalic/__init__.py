from listcondalic.liccheck_and_condameta_based import main as _main
import click

@click.command("List licenses and versions")
@click.argument('kind', help='Either conda or pip')
@click.argument('file', help='Dependency filename')
def main(kind, file):
    _main(kind=kind, file=file)


if __name__ == "__main__":
    main()
