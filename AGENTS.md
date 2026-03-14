# Agent Instructions for soundcloud-lib

## Project Overview

**soundcloud-lib** is a Python library providing a SoundCloud API wrapper that doesn't require a user-provided client ID — it automatically scrapes one from public SoundCloud pages.

- **License**: MIT
- **Python Version**: >=3.11
- **Repository**: https://github.com/JOGGIN-INC/soundcloud-lib

## Key Features

- Resolve tracks and playlists from URLs
- Download and write MP3 files with metadata (album, artist, title, artwork)
- Fetch entire playlists
- Async/await support via `sclib.asyncio`
- Automatic client ID scraping

## Project Structure

```
soundcloud-lib/
├── sclib/                  # Main library package
│   ├── sync.py            # Synchronous API (SoundcloudAPI, Track, Playlist, Likes)
│   ├── asyncio.py         # Asynchronous API (async variants of sync.py classes)
│   └── util.py            # Utilities (regex, HTML parsing, client ID extraction)
├── tests/
│   ├── test_smoke.py              # Basic import/instantiation tests
│   ├── test_error_handling.py     # Mocked error scenario tests
│   └── integration/               # Network-dependent tests (sync/ and async/)
├── pyproject.toml         # Project metadata & pytest config
├── requirements-dev.txt   # Dev dependencies (pytest, pytest-asyncio)
└── README.md             # User documentation
```

## Development Workflow

### Setup

```bash
pip install -e .
pip install -r requirements-dev.txt
```

### Testing

**IMPORTANT**: Tests MUST pass before creating a PR.

```bash
# Run unit tests (default, excludes integration tests)
pytest

# Run all tests including integration tests
pytest -m ""

# Run only integration tests
pytest -m integration
```

**Test Types**:
- **Unit tests** (`test_smoke.py`, `test_error_handling.py`): No network calls, always run in CI
- **Integration tests** (`tests/integration/`): Require network access, marked with `@pytest.mark.integration`, excluded from CI by default

### Linting

```bash
pip install -r requirements_dev.txt  # includes pylint
pylint sclib/
```

## Code Guidelines

### Testing Requirements

**All new code MUST be tested.** When adding functionality:

1. Add unit tests in `tests/test_*.py` for core logic
2. Use mocks to avoid network calls in unit tests
3. Add integration tests in `tests/integration/` only if testing actual API interactions
4. Follow existing test patterns (see `test_error_handling.py` for mock examples)

### Code Style

- Follow existing patterns in `sclib/sync.py` and `sclib/asyncio.py`
- Keep async implementation in sync with synchronous implementation
- Use type hints where present in existing code
- Handle errors gracefully (see `util.py:eprint()` for stderr output)

### Making Changes

1. **Read existing code** before modifying
2. **Run tests before changes** to establish baseline: `pytest`
3. **Make minimal, focused changes**
4. **Add tests for new functionality**
5. **Run tests after changes**: `pytest`
6. **Ensure tests pass** before creating PR

## Known Limitations

- Non-downloadable tracks cannot be downloaded (only have HLS streams, not supported)
- HLS stream assembly not currently supported

## Keeping This File Updated

**IMPORTANT**: When making changes to the repository, update this file if:

- Project structure changes (new directories, moved files)
- Testing approach changes (new test types, different test commands)
- Development workflow changes (new build steps, linting tools)
- New major features are added that agents should know about
- Dependencies or Python version requirements change

Keep descriptions concise. Focus on what agents need to know to work effectively.
