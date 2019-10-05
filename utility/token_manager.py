import functools
from datetime import datetime, timedelta

from jose import jwt

from zathura_bugtracker import settings
from utility.helper import get_user_object
from jose.exceptions import JWTError, JWTClaimsError, ExpiredSignatureError


def encode_access_token(username: str, role: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=16),
        'iat': datetime.utcnow(),
        'sub': username,
        'type': 'access',
        'role': role
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
    return token


def encode_refresh_token(username: str, role: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(days=5),
        'iat': datetime.utcnow(),
        'sub': username,
        'type': 'refresh',
        'role': role
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
    return token


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms='HS512')
    except ExpiredSignatureError:
        return None
    except JWTClaimsError:
        return None
    except JWTError:
        return None


def protected(function):
    @functools.wraps(function)
    def wrapper(self, request, *args, **kwargs):
        required = ('type', 'exp', 'sub', 'role')
        epoch = datetime.utcfromtimestamp(0)
        if 'access_token' not in request.COOKIES:
            # TODO: access_token is not present on cookies
            # TODO: logout here
            return None
        payload = decode_token(request.COOKIES['access_token'])

        if payload is None:
            return None
        # Validate user and access token expiry
        for field in required:
            if field not in payload:
                # TODO: generate a logout here.
                return None

        if payload['type'] != "access":
            # TODO: generate a logout here.
            return None

        if payload['exp'] < (datetime.utcnow() - epoch).total_seconds():
            # TODO: token has expired. hit refresh here.
            return None

        if get_user_object(username=payload["sub"]) is None:
            # TODO: USER does not exist (generate logout)
            return None
        return function(self, request, *args, **kwargs)
    return wrapper
