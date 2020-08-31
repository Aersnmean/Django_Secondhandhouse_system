import mongoengine


class User(mongoengine.Document):
    username = mongoengine.StringField()
    password = mongoengine.StringField()
    tel = mongoengine.StringField(unique=True)

    meta = {'collection': 'Users'}


class Publications(mongoengine.Document):
    tel = mongoengine.StringField()
    publist = mongoengine.ListField()

    meta = {'collection': 'Publications'}


class UserInfo(mongoengine.Document):
    tel = mongoengine.StringField()
    username = mongoengine.StringField()
    realname = mongoengine.StringField()
    gender = mongoengine.StringField()
    age = mongoengine.StringField()
    address = mongoengine.StringField()
    self_introduction = mongoengine.StringField()

    meta = {'collection': 'UserInfo'}
