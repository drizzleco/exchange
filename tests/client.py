import pytest
import tempfile
import os
import datetime
from backend import app as backend
from backend.schema import schema
from backend.models import User, Auction, Bid
from graphene.test import Client


@pytest.fixture
def graphql_client():
    db_fd, backend.app.config["DATABASE"] = tempfile.mkstemp()
    backend.app.config["TESTING"] = True
    with backend.app.app_context():
        backend.db.drop_all()
        backend.db.create_all()
        u1 = User(
            username="test",
            email="test@gmail.com",
            password="test",
            created=datetime.datetime.utcnow(),
        )
        a1 = Auction(
            name="test auction",
            description="test desc",
            starting_price=99.99,
            created=datetime.datetime.utcnow(),
            end_time=datetime.datetime.utcnow() + datetime.timedelta(days=7),
            user=u1,
        )
        b1 = Bid(
            amount=100.01,
            created=datetime.datetime(2020, 7, 13, 7, 43),
            user=u1,
            auction=a1,
        )
        backend.db.session.add(u1)
        backend.db.session.commit()
    yield Client(schema)
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
