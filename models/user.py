# models/user.py
# Simple user model for demonstration (replace with DB integration for production)

class UserModel:
    users = []  # In-memory user list for demo

    @classmethod
    def add_user(cls, email, password):
        cls.users.append({'email': email, 'password': password})

    @classmethod
    def find_user(cls, email):
        for user in cls.users:
            if user['email'] == email:
                return user
        return None

    @classmethod
    def validate_user(cls, email, password):
        user = cls.find_user(email)
        if user and user['password'] == password:
            return True
        return False
