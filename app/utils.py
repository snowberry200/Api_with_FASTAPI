from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def encrypt (password):
    return pwd_context.hash(password)

# COMPARING THE TWO HASHED (PASSWORDS)
def verify_passwords (encrypt, hashed_password):
    return pwd_context.verify(encrypt, hashed_password)