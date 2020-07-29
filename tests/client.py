import pytest
import tempfile
import os
from backend import app as backend


@pytest.fixture
def client():
    db_fd, backend.app.config["DATABASE"] = tempfile.mkstemp()
    backend.app.config["TESTING"] = True
    with backend.app.test_client() as client:
        with backend.app.app_context():
            backend.db.drop_all()
            backend.db.create_all()
        yield client
    os.close(db_fd)
    os.unlink(backend.app.config["DATABASE"])
