from rest_framework import status

token_expired = {
    'message': 'token_expired',
    'status_code': -100,
    'status': status.HTTP_406_NOT_ACCEPTABLE
}

token_invalid = {
    'message': 'token invalid',
    'status_code': -101,
    'status': status.HTTP_401_UNAUTHORIZED
}