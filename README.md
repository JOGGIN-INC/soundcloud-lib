# soundcloud-lib

A Python SoundCloud API wrapper that doesn't require a user-provided client ID — it scrapes one from public SoundCloud pages.

Hard-forked from [3jackdaws/soundcloud-lib](https://github.com/3jackdaws/soundcloud-lib).

## Installation

```bash
pip install git+https://github.com/JOGGIN-INC/soundcloud-lib.git
```

## Features

- Resolve tracks and playlists from URLs
- Download and write MP3 representation of a track to a file
- Fetches and writes MP3 metadata (album artist, title, artwork)
- Fetch entire playlists of tracks
- Asyncio support via `sclib.asyncio`

## Usage

### Save an MP3 to a file

```python
from sclib import SoundcloudAPI, Track, Playlist

api = SoundcloudAPI()
track = api.resolve('https://soundcloud.com/itsmeneedle/sunday-morning')

assert type(track) is Track

with open(f'./{track.artist} - {track.title}.mp3', 'wb+') as f:
    track.write_mp3_to(f)
```

### Fetch a playlist

```python
from sclib import SoundcloudAPI, Track, Playlist

api = SoundcloudAPI()
playlist = api.resolve('https://soundcloud.com/some-user/some-playlist')

assert type(playlist) is Playlist

for track in playlist.tracks:
    with open(f'./{track.artist} - {track.title}.mp3', 'wb+') as f:
        track.write_mp3_to(f)
```

### Async usage

```python
from sclib.asyncio import SoundcloudAPI, Track

async def main():
    api = SoundcloudAPI()
    track = await api.resolve('https://soundcloud.com/itsmeneedle/sunday-morning')
    with open(f'./{track.artist} - {track.title}.mp3', 'wb+') as f:
        await track.write_mp3_to(f)
```

## License

MIT
