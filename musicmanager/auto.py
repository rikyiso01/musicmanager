from pathlib import Path
from typing import Optional
from musicmanager.download import download
from musicmanager.neobackup import neobackup
from os import environ


def auto(playlists: list[str], folder: Optional[Path] = None):
    if folder is None:
        folder = Path(environ["XDG_MUSIC_DIR"])
    neobackup_folder = folder / "neobackup"
    newpipe_folder = folder / "newpipe"
    songs_folder = folder / "songs"
    playlists_folder = folder / "playlists"
    neobackup(neobackup_folder, newpipe_folder)
    for playlist in playlists:
        playlist_file = f"{playlist}.m3u"
        download(
            newpipe_folder / playlist_file,
            songs_folder,
            playlists_folder / playlist_file,
        )
