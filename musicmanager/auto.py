from pathlib import Path
from tomllib import load
from pydantic import TypeAdapter
from dataclasses import dataclass

from musicmanager.download import download
from musicmanager.newpipetom3u import newpipetom3u

@dataclass
class Config:
    newpipe_playlists_dir:Path
    playlists:list[Path]
    playlists_dir:Path
    songs_dir:Path



def auto(file:Path,newpipe:Path):
    with file.open('rb') as f:
        config=load(f)
    config=TypeAdapter(Config).validate_python(config)
    newpipetom3u(newpipe,config.newpipe_playlists_dir)
    for playlist in config.playlists:
        download(config.newpipe_playlists_dir/f"{playlist}.m3u",config.songs_dir,config.playlists_dir/f"{playlist}.m3u")
