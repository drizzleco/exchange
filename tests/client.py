import pytest
import tempfile
import os
import datetime
from backend import app as backend
from backend.schema import schema
from backend.tests import u1
from graphene.test import Client


def create_test_data():
    db_fd, backend.app.config["DATABASE"] = tempfile.mkstemp()
    backend.app.config["TESTING"] = True
    with backend.app.test_client() as client:
        with backend.app.app_context():
            backend.db.drop_all()
            backend.db.create_all()
            backend.db.session.add(u1)
            backend.db.session.commit()
        yield client
    os.close(db_fd)
    os.unlink(backend.app.config["DATABASE"])


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


graphql_client = Client(schema)
