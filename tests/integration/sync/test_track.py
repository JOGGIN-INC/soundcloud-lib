""" Test Sync Track object """

import os
from io import BytesIO
from urllib.request import urlopen

import mutagen
import pytest

from sclib.sync import SoundcloudAPI, Track
from sclib.util import get_large_artwork_url

from tests.integration.sync.test_api import sc_client  # pylint: disable=unused-import


TEST_TRACK_URL = 'https://soundcloud.com/mt-marcy/cold-nights'
TEST_TRACK_TITLE = 'cold nights'
TEST_TRACK_ARTIST = 'mt. marcy'


@pytest.fixture(name='test_track')
def track_fixture(sync_api):
    """ Example track """
    sync_api = SoundcloudAPI()
    return sync_api.resolve(TEST_TRACK_URL)


@pytest.mark.integration
def test_resolve_track(sync_api: SoundcloudAPI):
    track = sync_api.resolve(TEST_TRACK_URL)
    assert type(track) is Track

@pytest.mark.integration
def test_track_has_correct_attributes(test_track: Track):
    assert test_track.title == TEST_TRACK_TITLE
    assert test_track.artist == TEST_TRACK_ARTIST

@pytest.mark.integration
def test_track_accepts_correct_file_objects(sync_api: SoundcloudAPI):
    track = sync_api.resolve(TEST_TRACK_URL)
    filename = os.path.realpath('faksjhflaksjfhlaksjfdhlkas.mp3')
    with open(filename, 'wb+') as mp3:
        track.write_mp3_to(mp3)
    os.remove(filename)

    with open(filename, 'w'):
        pass
    try:
        with open(filename, 'rb+') as mp3:
            track.write_mp3_to(mp3)
    finally:
        os.remove(filename)

    try:
        with open(filename, 'w') as file:
            track.write_mp3_to(file)
    except TypeError:
        pass

    try:
        with open(filename, 'wb') as file:
            track.write_mp3_to(file)
    except ValueError:
        pass
    finally:
        os.remove(filename)

    file = BytesIO()
    track.write_mp3_to(file)
    assert file.__sizeof__() > 0

@pytest.mark.integration
def test_track_writes_mp3_metadata(test_track: Track):
    filename = 'test_track.mp3'
    with open(filename, 'wb+') as file:
        test_track.write_mp3_to(file)
    mp3 = mutagen.File(filename)
    tags = mp3.tags
    assert tags['TIT2'] == TEST_TRACK_TITLE
    assert tags['TPE1'] == TEST_TRACK_ARTIST
    cover_art = tags['APIC:Cover']
    with urlopen(get_large_artwork_url(test_track.artwork_url)) as client:
        assert cover_art.data == client.read()
    os.remove(filename)

@pytest.mark.integration
def test_track_writes_mp3_album(sync_api):
    track = sync_api.resolve('https://soundcloud.com/if2l/2-months')
    assert type(track) == Track
    track.album = 'Made in Abyss OST'
    track.artist = 'Kevin Pekin'
    track.track_no = ":^)"
    filename = f'{track.artist} - {track.title}.mp3'
    try:
        with open(filename, 'wb+') as file:
            track.write_mp3_to(file)
    finally:
        os.remove(filename)

@pytest.mark.integration
def test_fetch_track_by_id_in_order(sync_api: SoundcloudAPI):
    expected = [222820656, 1860005124, 289589592, 268448230]
    tracks = sync_api.get_tracks(*expected)
    actual = [t['id'] for t in tracks]
    assert expected == actual
