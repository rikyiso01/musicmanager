from typer import Typer
from musicmanager.newpipetom3u import newpipetom3u
from musicmanager.download import download
from musicmanager.neobackup import neobackup
from musicmanager.auto import auto

app = Typer()

programs = [newpipetom3u, download, neobackup, auto]

for program in programs:
    app.command()(program)


def entry():
    app()


if __name__ == "__main__":
    entry()
