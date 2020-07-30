from client import graphql_client


def test_resolve_users(graphql_client):
    executed = graphql_client.execute(
        """
        {
            users(username: "test") {
                id
                username
                auctions {
                name
                description
                bids {
                    id
                    amount
                }
                }
            }
        }
        """
    )
    assert executed == {
        "data": {
            "users": [
                {
                    "id": "1",
                    "username": "test",
                    "auctions": [
                        {
                            "name": "test auction",
                            "description": "test desc",
                            "bids": [{"id": "1", "amount": 100.01},],
                        }
                    ],
                }
            ]
        }
    }


def test_resolve_auctions(graphql_client):
    executed = graphql_client.execute(
        """
        {
        auctions {
            id
            name
            startingPrice
            description
            bids {
            id
            amount

            }
        }
        }

        """
    )
    assert executed == {
        "data": {
            "auctions": [
                {
                    "id": "1",
                    "name": "test auction",
                    "startingPrice": 99.99,
                    "description": "test desc",
                    "bids": [{"id": "1", "amount": 100.01},],
                }
            ]
        }
    }


def test_resolve_bid(graphql_client):
    executed = graphql_client.execute(
        """
        {
        bid(id: 1) {
            id
            amount
            user {
            username
            }
            auction {
            name
            description
            }
        }
        }

        """
    )
    assert executed == {
        "data": {
            "bid": {
                "id": "1",
                "amount": 100.01,
                "user": {"username": "test"},
                "auction": {"name": "test auction", "description": "test desc"},
            }
        }
    }

