import datetime

import graphene
from flask_login import current_user
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphql import GraphQLError
from helpers import toDateObj
from models import Auction as AuctionModel
from models import Bid as BidModel
from models import User as UserModel
from models import db


class User(SQLAlchemyObjectType):
    """
    User Model
    """

    class Meta:
        model = UserModel
        exclude_fields = ("email",)


class Auction(SQLAlchemyObjectType):
    """
    Auction Model
    """

    class Meta:
        model = AuctionModel


class Bid(SQLAlchemyObjectType):
    """
    Bid Model
    """

    class Meta:
        model = BidModel


class Query(graphene.ObjectType):
    """
    Base Query
    """

    users = graphene.List(
        User,
        id=graphene.Int(),
        username=graphene.String(),
        page=graphene.Int(),
        limit=graphene.Int(),
    )

    def resolve_users(self, info, **args):
        """
        Parse user query and return data
        """
        page_size = args.get("limit", 10)
        offset = args.get("page", 0) * page_size
        fuzzy_query = {}
        for query in ["id", "username"]:
            fuzzy_query[query] = "%{}%".format(args.get(query, ""))
        return (
            User.get_query(info)
            .filter(
                db.or_(UserModel.id.like(fuzzy_query["id"])),
                db.or_(UserModel.username.like(fuzzy_query["username"])),
            )
            .order_by(db.asc(UserModel.username))
            .offset(offset)
            .limit(page_size)
        )

    auctions = graphene.List(
        Auction,
        id=graphene.Int(),
        name=graphene.String(),
        description=graphene.String(),
        starting_price=graphene.Float(),
        end_time=graphene.String(),
        page=graphene.Int(),
        limit=graphene.Int(),
    )

    def resolve_auctions(self, info, **args):
        """
        Parse auction query and return data
        """
        page_size = args.get("limit", 10)
        offset = args.get("page", 0) * page_size
        fuzzy_query = {}
        for query in ["id", "name", "description", "starting_price", "end_time"]:
            fuzzy_query[query] = "%{}%".format(args.get(query, ""))
        return (
            Auction.get_query(info)
            .filter(
                db.or_(AuctionModel.id.like(fuzzy_query["id"])),
                db.or_(AuctionModel.name.like(fuzzy_query["name"])),
                db.or_(AuctionModel.description.like(fuzzy_query["description"])),
                db.or_(AuctionModel.starting_price).like(fuzzy_query["starting_price"]),
                db.or_(AuctionModel.end_time.like(fuzzy_query["end_time"])),
            )
            .order_by(db.asc(AuctionModel.id))
            .offset(offset)
            .limit(page_size)
        )

    bid = graphene.Field(Bid, id=graphene.Int(),)

    def resolve_bid(self, info, **args):
        """
        Parse bid query and return data
        """
        return Bid.get_query(info).filter_by(id=args.get("id")).first()


class CreateAuction(graphene.Mutation):
    """
    Create Auction mutation
    """

    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        starting_price = graphene.Float(required=True)
        end_time = graphene.String(required=True)

    auction = graphene.Field(lambda: Auction)
    message = graphene.String()

    def mutate(self, info, **args):
        name = args.get("name")
        description = args.get("description")
        if not name or not description:
            raise GraphQLError("Name/Description cannot be blank!")
        end_time = toDateObj(args.get("end_time"))
        if end_time <= datetime.datetime.utcnow():
            raise GraphQLError("Your auction can't end in the past! LOL")
        starting_price = args.get("starting_price")
        if starting_price < 0:
            raise GraphQLError("Starting price can't be negative!")

        auction = AuctionModel(
            name=name,
            description=description,
            starting_price=starting_price,
            created=datetime.datetime.utcnow(),
            end_time=end_time,
            user=current_user,
        )
        message = "Auction created successfully!"
        db.session.add(auction)
        db.session.commit()
        return CreateAuction(auction=auction, message=message)


class CreateBid(graphene.Mutation):
    """
    Create Bid mutation
    """

    class Arguments:
        auction_id = graphene.Int(required=True)
        amount = graphene.Float(required=True)

    bid = graphene.Field(lambda: Bid)
    message = graphene.String()

    def mutate(self, info, **args):
        auction = AuctionModel.query.filter_by(id=args.get("auction_id")).first()
        if not auction:
            raise GraphQLError("Oops! That auction was not found")
        if auction.user == current_user:
            raise GraphQLError("You can't bid on your own auction!!")
        if args.get("amount") <= auction.get_current_price():
            raise GraphQLError(
                "Your bid must be higher than the current price: "
                + str(auction.get_current_price())
            )

        bid = BidModel(
            auction=auction,
            amount=args.get("amount"),
            created=datetime.datetime.utcnow(),
            user=current_user,
        )
        message = "Bid created successfully!"
        db.session.add(bid)
        db.session.commit()
        return CreateBid(bid=bid, message=message)


class Mutation(graphene.ObjectType):
    create_auction = CreateAuction.Field()
    create_bid = CreateBid.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
