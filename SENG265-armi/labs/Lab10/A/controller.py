import hashlib

class Controller:
    def __init__(self):
        self.products = []
        self.users = self.load_users()
        self.logged = False

    def load_users(self):
        users = {}
        with open('users.txt', 'r') as file:
            for line in file:
                tokens = line.strip().split(',')
                users[tokens[0]] = tokens[1]
            return users

    def get_password_hash(self, password):
        encoded_password = password.encode('utf-8')     # Convert the password to bytes
        hash_object = hashlib.sha256(encoded_password)      # Choose a hashing algorithm (e.g., SHA-256)
        hex_dig = hash_object.hexdigest()       # Get the hexadecimal digest of the hashed password
        return hex_dig

    def login(self, username, password):
        if self.users.get(username):
            password_hash = self.get_password_hash(password)
            if self.users.get(username) == password_hash:
                self.logged = True
                return True
            else:
                return False
        else:
            return False



