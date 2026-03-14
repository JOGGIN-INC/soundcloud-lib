"""
Smoke tests — no network calls, just verify the package imports and instantiates correctly.
These are the only tests that run in CI. For live API tests, run: pytest -m integration
"""
from sclib import SoundcloudAPI
from sclib.sync import SoundcloudAPI as SyncAPI
from sclib.asyncio import SoundcloudAPI as AsyncAPI


def test_sync_api_instantiates():
    api = SyncAPI()
    assert api is not None


def test_async_api_instantiates():
    api = AsyncAPI()
    assert api is not None


def test_package_exports_soundcloud_api():
    api = SoundcloudAPI()
    assert api is not None
