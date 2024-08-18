from typing import IO
from collections.abc import Mapping,Sequence

type M3U=Sequence[Mapping[str|None,str|None]]

def dump(content:M3U, fd: IO[str]):
    fd.write("#EXTM3U\n")
    for entry in content:
        for key, value in entry.items():
            line:str
            if key is None:
                assert value is not None
                line=value
            elif value is not None:
                line=f"#{key}:{value}"
            else:
                line=f"#{key}"
            fd.write(f"{line}\n")

def load(fd:IO[str])->list[dict[str|None,str|None]]:
    assert fd.readline().strip()=="#EXTM3U"
    result:list[dict[str|None,str|None]]=[]
    buffer:dict[str,str|None]={}
    for line in fd:
        line=line.strip()
        if not line:
            continue
        if line.startswith('#'):
            if ":" in line:
                buffer[line[1:line.index(":")]]=line[line.index(":")+1:]
            else:
                buffer[line[1:]]=None
            continue
        if '#' in line:
            line=line[:line.index("#")]
        result.append(buffer|{None:line})
    return result

