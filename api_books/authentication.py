import jwt
from rest_framework import exceptions
from datetime import datetime, timedelta, timezone

def create_access_token(id):
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=30)
    
    return jwt.encode({
        'user_id': id,
        'exp': expiration,
        'iat': now
    }, 'access_secret', algorithm='HS256')
    
def create_refresh_token(id):
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(minutes=30)
    
    return jwt.encode({
        'user_id': id,
        'exp': expiration,
        'iat': now
    }, 'refresh_secret', algorithm='HS256')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        return payload['user_id']
    except Exception as e:
        raise exceptions.AuthenticationFailed('unauthenticated')

    
   
