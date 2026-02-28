class User:
    def __init__(self, user_id, username, password, phone_number):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.phone_number = phone_number

    def __repr__(self):
        return f'User(user_id: {self.user_id}, username: {self.username}, password: {self.password}, phone_number: {self.phone_number})'