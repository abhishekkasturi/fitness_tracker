from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    """
    Converts a plain password into a secure hash
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    """
    Checks if the entered password matches the stored hash
    """
    return pwd_context.verify(password, hashed_password)