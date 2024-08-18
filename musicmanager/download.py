from pathlib import Path
from musicmanager.m3u import dump, load
from subprocess import call
from os import environ
from tqdm import tqdm

def get_youtube_url(id:str):
    return f"https://www.youtube.com/watch?v={id}"

YOUTUBE_DL=environ.get("YOUTUBE_DL","yt-dlp")

def download(playlist:Path,outdir:Path,output:Path):
    with playlist.open('rt') as f:
        m3u=load(f)
    result:list[dict[str|None,str|None]]=[]
    for song in tqdm(m3u):
        new_entry:dict[str|None,str|None]={}
        if "PLAYLIST" in song:
            new_entry["PLAYLIST"]=song["PLAYLIST"]
        new_entry["EXTINF"]=song["EXTINF"]
        new_entry["MOOSINF"]="LOCAL"
        url=song[None]
        assert url is not None
        id=url[url.index('?')+3:url.index('&') if '&' in url else len(url)]
        outfile=ensure_id(id,outdir)
        if outfile is None:
            continue
        new_entry[None]=str(outfile.absolute().relative_to(output.parent.absolute(),walk_up=True))
        result.append(new_entry)
    with output.open('wt') as f:
        dump(result,f)

def ensure_id(id:str,outdir:Path)->Path|None:
    blocked_file=outdir/f"{id}.blocked"
    if blocked_file.exists():
        return None
    for f in outdir.iterdir():
        if id in f.name:
            return f
    exitcode=call([YOUTUBE_DL,"--no-playlist","--extract-audio","--add-metadata","--embed-thumbnail",get_youtube_url(id)],cwd=outdir)
    if exitcode==1:
        blocked_file.touch()
        return None
    elif exitcode!=0:
        assert False
    for f in outdir.iterdir():
        if id in f.name:
            return f
    assert False
