"""
Test sync playlists
"""
import pytest
from sclib.sync import SoundcloudAPI


@pytest.fixture(name='sclib')
def sclib_fixture():
    return SoundcloudAPI()


@pytest.mark.integration
@pytest.mark.parametrize("playlist_url", [
    "https://soundcloud.com/soundcloud-circuits/sets/web-tempo-future-dance-and-electronic",
    "https://soundcloud.com/discover/sets/artist-stations:127466931",
])
def test_playlist_is_resolved(sclib: SoundcloudAPI, playlist_url: str):
    sclib.resolve(playlist_url)


@pytest.mark.integration
@pytest.mark.parametrize("playlist_url,expected_playlist_kind", [
    ("https://soundcloud.com/soundcloud-circuits/sets/web-tempo-future-dance-and-electronic", "playlist"),
    # artist-stations kind is unstable — SoundCloud changes this endpoint's response occasionally
    pytest.param(
        "https://soundcloud.com/discover/sets/artist-stations:127466931", "system-playlist",
        marks=pytest.mark.xfail(reason="SoundCloud artist-station type is unstable", strict=False)
    ),
])
def test_playlist_type(sclib: SoundcloudAPI, playlist_url: str, expected_playlist_kind: str):
    test_playlist = sclib.resolve(playlist_url)
    assert test_playlist.kind == expected_playlist_kind
