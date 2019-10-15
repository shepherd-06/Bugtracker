import functools
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import reverse, redirect
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTClaimsError, JWTError

from utility.helper import get_user_object, set_cookie
from zathura_bugtracker import settings


def encode_access_token(username: str, role: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=1),
        'iat': datetime.utcnow(),
        'sub': username,
        'type': 'access',
        'role': role
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
    return token


def encode_refresh_token(username: str, role: str):
    payload = {
        'exp': datetime.utcnow() + timedelta(minutes=5),
        'iat': datetime.utcnow(),
        'sub': username,
        'type': 'refresh',
        'role': role
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
    return token


def decode_token(token: str):
    """
    # TODO: generate a message here for exception occurring.
    decodes access and refresh token here.
    """
    try:
        _ = jwt.decode(token, settings.SECRET_KEY, algorithms='HS512')
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("decode_token")
        print(_)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        return _
    except ExpiredSignatureError:
        return HttpResponseRedirect(reverse("index"))
    except JWTClaimsError:
        return HttpResponseRedirect(reverse("index"))
    except JWTError:
        return HttpResponseRedirect(reverse("index"))


def check_refresh_token(request):
    """
    # TODO: generate a message here.
    After successful refresh token, redirect to the same page.
    Or sow appropriate error message | request to login again.
    """
    if 'refresh_token' not in request.COOKIES:
        return HttpResponseRedirect(reverse("index"))

    print("Refresh Token hits")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(request.COOKIES['refresh_token'])
    payload = decode_token(request.COOKIES['refresh_token'])
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    required = ('type', 'exp', 'sub', 'role')
    epoch = datetime.utcfromtimestamp(0)

    for field in required:
        if field not in payload:
            return HttpResponseRedirect(reverse("index"))

    if payload['type'] != "refresh":
        return HttpResponseRedirect(reverse("index"))

    if get_user_object(username=payload["sub"]) is None:
        return HttpResponseRedirect(reverse("index"))

    user = get_user_object(username=payload["sub"])

    if payload['exp'] < (datetime.utcnow() - epoch).total_seconds():
        # Refresh token also expired. Re-login is needed.
        return HttpResponseRedirect(reverse("index"))
    else:
        # Refresh token is still valid.
        access_token = str(encode_access_token(user.username, "user"))
        refresh_token = str(encode_refresh_token(user.username, "user"))

        print("Token refreshed. Redirect to: {}".format(request.path))
        response = HttpResponseRedirect(request.path)
        expiry = datetime.utcnow() + timedelta(hours=5)
        set_cookie(response, "access_token",
                   access_token, expired_at=expiry)
        set_cookie(response, "refresh_token", refresh_token)
        # successful refresh token, redirect to the same page
        return response


def protected(function):
    @functools.wraps(function)
    def wrapper(self, request, *args, **kwargs):
        """
        # TODO: for failed token, generate a message on screen
        """
        print("Hits access token")
        required = ('type', 'exp', 'sub', 'role')
        epoch = datetime.utcfromtimestamp(0)
        if 'access_token' not in request.COOKIES:
            return HttpResponseRedirect(reverse("index"))

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("|||||||||ACCESS TOKEN CHECK|||||||||")
        payload = decode_token(request.COOKIES['access_token'])
        print(request.COOKIES['access_token'])
        print(payload)
        print("||||||||||||||||||||||||||||||||||||")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        # Validate user and access token expiry
        for field in required:
            if field not in payload:
                return HttpResponseRedirect(reverse("index"))

        if payload['type'] != "access":
            return HttpResponseRedirect(reverse("index"))

        if get_user_object(username=payload["sub"]) is None:
            return HttpResponseRedirect(reverse("index"))

        if payload['exp'] < (datetime.utcnow() - epoch).total_seconds():
            # Access token is expired. Checks up refresh token
            check_refresh_token(request)

        return function(self, request, *args, **kwargs)
    return wrapper
