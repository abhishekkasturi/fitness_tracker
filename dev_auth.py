import os

# Admin password stored in environment variables
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def verify_admin(password: str):
    """
    Verify developer/admin login
    """

    if password == ADMIN_PASSWORD:
        return True

    return False