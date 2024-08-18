from pathlib import Path
from sqlite3 import connect, Cursor
from zipfile import ZipFile
from tempfile import TemporaryDirectory
from dataclasses import asdict, dataclass, field, fields
from musicmanager.m3u import dump


DATABASE_FILE = "newpipe.db"


@dataclass(kw_only=True)
class Song:
    url: str
    title: str
    thumbnail_url: str
    duration: int

    def to_m3u(self):
        return {
            "EXTINF": f"{self.duration},{self.title}",
            "EXTIMG": self.thumbnail_url,
            "MOOSINF": "YOUTUBE",
            None: self.url,
        }


@dataclass
class Playlist:
    title: str
    songs: list[Song] = field(default_factory=list)

    def to_m3u(self):
        songs = [song.to_m3u() for song in self.songs]
        songs[0]={"PLAYLIST":self.title}|songs[0]
        return songs


@dataclass
class PlaylistDB:
    uid: int
    name: str


@dataclass
class StreamDB:
    url: str
    title: str
    duration: int
    thumbnail_url: str
    playlist_id: int

    def to_song(self):
        content = asdict(self)
        del content["playlist_id"]
        return Song(**content)


def newpipetom3u(path: Path, outdir: Path):
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        with ZipFile(path) as file:
            file.extract(DATABASE_FILE, tmpdir)
            extract_database(tmpdir/DATABASE_FILE,outdir)

def extract_database(file:Path,outdir:Path):
    with connect(file) as connection:
        cursor = connection.cursor()
        playlists = get_playlists(cursor)
    for playlist in playlists:
        out = outdir / f"{playlist.title}.m3u"
        with out.open("wt") as f:
            dump(playlist.to_m3u(), f)

def read_playlists(cursor: Cursor):
    return [
        PlaylistDB(*entry)
        for entry in cursor.execute(
            f"select {','.join(f.name for f in fields(PlaylistDB))} from playlists"
        )
    ]


def read_playlists_content(cursor: Cursor):
    return [
        StreamDB(*entry)
        for entry in cursor.execute(
            f"select {','.join(f.name for f in fields(StreamDB))} from streams join playlist_stream_join on uid=stream_id order by join_index"
        )
    ]


def get_playlists(cursor: Cursor):
    playlists = read_playlists(cursor)
    playlist_content = read_playlists_content(cursor)
    result = {playlist.uid: Playlist(playlist.name) for playlist in playlists}
    for content in playlist_content:
        result[content.playlist_id].songs.append(content.to_song())
    return [*result.values()]

