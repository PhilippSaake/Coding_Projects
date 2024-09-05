import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import secrets

def write_key(key):
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()


def generate_keyfile(password): 
    temp_password = str(password).encode()  # Convert to type bytes
    salt = secrets.token_bytes(16)  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=100000,
    backend=default_backend()
    )
    temp_key = base64.urlsafe_b64encode(kdf.derive(temp_password))
    write_key(temp_key)

def encode_message(message):
    key = load_key()
    f = Fernet(key)
    return(f.encrypt(message.encode()))

def decode_message(message):
    key = load_key()
    f = Fernet(key)
    return(f.decrypt(message).decode())