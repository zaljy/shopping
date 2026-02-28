import bcrypt

def hash_password(password):
    password = "user_password".encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed_password