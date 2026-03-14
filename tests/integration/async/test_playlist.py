"""
Test async playlists
"""
import pytest
from sclib.asyncio import SoundcloudAPI

pytest_plugins = ('pytest_asyncio',)


@pytest.fixture(name='sclib')
def sclib_fixture():
    return SoundcloudAPI()


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.parametrize("playlist_url", [
    "https://soundcloud.com/soundcloud-circuits/sets/web-tempo-future-dance-and-electronic",
    "https://soundcloud.com/discover/sets/artist-stations:127466931",
])
async def test_playlist_is_resolved(sclib: SoundcloudAPI, playlist_url: str):
    await sclib.resolve(playlist_url)


@pytest.mark.integration
@pytest.mark.asyncio
@pytest.mark.parametrize("playlist_url,expected_playlist_kind", [
    ("https://soundcloud.com/soundcloud-circuits/sets/web-tempo-future-dance-and-electronic", "playlist"),
    pytest.param(
        "https://soundcloud.com/discover/sets/artist-stations:127466931", "system-playlist",
        marks=pytest.mark.xfail(reason="SoundCloud artist-station type is unstable", strict=False)
    ),
])
async def test_playlist_type(sclib: SoundcloudAPI, playlist_url: str, expected_playlist_kind: str):
    test_playlist = await sclib.resolve(playlist_url)
    assert test_playlist.kind == expected_playlist_kind
