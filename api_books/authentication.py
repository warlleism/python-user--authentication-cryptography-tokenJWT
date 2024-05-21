import jwt
from datetime import datetime, timedelta, timezone

def create_access_token(id):
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(seconds=30)
    
    return jwt.encode({
        'user_id': id,
        'exp': expiration,
        'iat': now
    }, 'access_secret', algorithm='HS256')
    
def create_refresh_token(id):
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(seconds=30)
    
    return jwt.encode({
        'user_id': id,
        'exp': expiration,
        'iat': now
    }, 'refresh_secret', algorithm='HS256')
