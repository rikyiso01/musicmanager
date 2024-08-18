from typer import Typer
from musicmanager.newpipetom3u import newpipetom3u
from musicmanager.download import download

app=Typer()

programs=[newpipetom3u,download]

for program in programs:
    app.command()(program)

def entry():
    app()


if __name__=="__main__":
    entry()

