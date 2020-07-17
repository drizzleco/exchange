import datetime

from models import Auction, Bid, User, db

db.drop_all()
db.create_all()

u1 = User(username="test", email="test@gmail.com", created=datetime.datetime.utcnow(),)
u1.set_password("test")
a1 = Auction(
    name="test auction",
    description="test desc",
    starting_price=99.99,
    created=datetime.datetime.utcnow(),
    end_time=datetime.datetime.utcnow() + datetime.timedelta(days=7),
    user=u1,
)
b1 = Bid(
    amount=100.01, created=datetime.datetime(2020, 7, 13, 7, 43), user=u1, auction=a1,
)
b2 = Bid(amount=220, created=datetime.datetime.utcnow(), user=u1, auction=a1,)
db.session.add(u1)
db.session.commit()
