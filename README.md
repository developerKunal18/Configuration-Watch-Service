# Configuration Watch Service

Flask service for watching versioned configuration changes.

## Features
- Versioned configuration
- Configuration change history
- Query changes since a version
- Thread-safe storage
- Validation
- Tests

## Run
```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```

Endpoints:
- PUT `/api/config/<service>`
- GET `/api/config/<service>`
- GET `/api/config/<service>/changes?since=<version>`
- GET `/health`

Run tests:
```bash
pytest
```

> Educational in-memory implementation. Production systems should use durable storage and an event/message system for reliable propagation.
