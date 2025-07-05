# utils/auth.py
from flask_login import UserMixin
from models.user import UserModel

class AppUser(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

    @staticmethod
    def get_by_email(email):
        user = UserModel.find_user(email)
        if user:
            return AppUser(user['email'], user['email'])
        return None
