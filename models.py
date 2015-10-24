import datetime

from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin
from peewee import *
from lets_deal_with_images_tonight import *

DATABASE = SqliteDatabase('storage.db')

class BaseModel(Model):
    class Meta:
        database = DATABASE





class User(BaseModel, UserMixin):
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)
    confirmed_email = BooleanField(default=False)
    confirmed_on = DateTimeField(default=datetime.datetime.now())
    # reviews = TextField(null=True)
    review1 = TextField(null= True)
    #do i really need confirmed on?
    #keep it and try it out?
    #but it also makes your db bigger?
    # lets give it a shot


    #important revisit with expert

    # def is_admin(self):
    #     return self.is_admin
    # def is_active(self): # line 37
    #     return True


    @classmethod
    def create_user(cls, username, first_name, last_name, email, password, is_admin=False, confirmed_email=False ):
        try:
            with DATABASE.transaction():
                cls.create(
                    username = username,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = generate_password_hash(password),
                    is_admin = is_admin,
                    confirmed_email = confirmed_email
                    # confirmed_on = datetime.datetime.now
                    )
        except IntegrityError:
            raise ValueError("We already have a user exactly like that dude. Try again")

    class Meta:
        order_by = ('-joined_at',)







class BuyListing(BaseModel):

    user = ForeignKeyField(rel_model = User, related_name='buy_space')
    created_at = DateTimeField(default=datetime.datetime.now)
    cubic_feet = CharField()  # restrict the storage to just small Medium large extra large
    bid = FloatField() # should be the prices of the fields
    what_user_needs = TextField(null=True)

    class Meta:
        order_by = ('-created_at',)

class SellListing(BaseModel):
    user = ForeignKeyField(rel_model = User, related_name='sell_space')
    created_at = DateTimeField(default=datetime.datetime.now)
    cubic_feet_avail = FloatField()
    ask = FloatField()
    what_user_is_offering = TextField() #Not optional
    pic_of_space = BlobField(null=True)





    class Meta:
        order_by = ('-created_at',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User,BuyListing, SellListing],safe=True)
    DATABASE.close()
