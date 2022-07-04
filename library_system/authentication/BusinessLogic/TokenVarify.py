
from authentication.models import User


def is_authenticated_user(email, token):
    user = User.objects.filter(email=email).first()
    if user:
        if user.token == token:
            return True
        return False
    return False
