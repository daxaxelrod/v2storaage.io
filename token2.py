# project/token.py

from itsdangerous import URLSafeTimedSerializer

# from storaage import app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer("my_super_precious")
    return serializer.dumps(email, salt="my_super_precious_two")


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('my_super_precious')
    try:
        email = serializer.loads(
            token,
            salt='my_super_precious_two',
            max_age=expiration
        )
    except:
        return False
    return email
