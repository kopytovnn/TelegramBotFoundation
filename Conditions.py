from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.sql import exists
from database.models.user import *


class Condition:
    def __init__(self, user):
        self.engine = create_engine("sqlite:///database/Data.db")
        Base.metadata.create_all(self.engine)
        self.user = user
        self.exodus = {

        }

    def condition(self, *args):
        if self:
            return True
        return False

    def check(self):
        answer = self.condition()
        return self.exodus[answer]


class UserIsSubscribed(Condition):
    def __init__(self, user, channel):
        super().__init__(user)
        self.channel = channel
        self.exodus = {
            True: True,
            False: True
        }

    def condition(self):
        if self.channel:  # !
            return True
        return False


class UserHavePremium(Condition):
    def __init__(self, user, msg1='User is a premium user', msg2='User is not a premium user'):
        super().__init__(user)
        self.exodus = {
            True: msg1,
            False: msg2
        }

    def condition(self):
        status = self.user.status
        if status == 'premium':
            return True
        return False


class UserIsRegistered(Condition):
    def __init__(self, telegram_id):
        super().__init__(None)
        self.telegram_id = telegram_id
        self.exodus = {
            True: True,
            False: False
        }

    def condition(self):
        with Session(self.engine) as session:
            isRegistered = session.query(exists().where(User.telegram_id == str(self.telegram_id))).scalar()
            return isRegistered
