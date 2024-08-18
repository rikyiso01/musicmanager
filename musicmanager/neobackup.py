from pathlib import Path
from subprocess import check_call
from tempfile import TemporaryDirectory
from musicmanager.newpipetom3u import extract_database
from sys import exit

DATABASE_FILE="databases/newpipe.db"

def neobackup(dir: Path, outpath: Path):
    for folder in dir.iterdir():
        if not folder.is_dir():
            continue
        if folder.name.startswith("."):
            continue
        operate(folder/"data.tar.zst",outpath)
    assert False

def operate(file:Path,outdir:Path):
    with TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        check_call(
            [
                "tar",
                "--use-compress-program=unzstd",
                "-xvf",
                str(file),
                "-C",str(tmp)
            ]
        )
        extract_database(tmp/DATABASE_FILE,outdir)
    exit(0)
