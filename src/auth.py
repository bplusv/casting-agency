import os
from functools import wraps
import json
import enum

from flask import request, _request_ctx_stack, abort
from urllib.request import urlopen
from jose import jwt


class UserRole(enum.Enum):
    CASTING_ASSISTANT = 1
    CASTING_DIRECTOR = 2
    EXECUTIVE_PRODUCER = 3


class Auth:
    @staticmethod
    def get_token_auth_header():
        auth = request.headers.get('Authorization', None)
        if not auth:
            abort(401, description='Unauthorized: Authorization '
                                   'header is expected')
        parts = auth.split()
        if parts[0].lower() != 'bearer':
            abort(401, description='Unauthorized: Authorization header '
                                   'must start with bearer')
        elif len(parts) == 1:
            abort(401, description='Unauthorized: Token not found')
        elif len(parts) > 2:
            abort(401, description='Unauthorized: Authorization header '
                                   'must be bearer token')
        token = parts[1]
        return token

    @staticmethod
    def check_permissions(permission, payload):
        if 'permissions' not in payload:
            abort(403, description='Forbidden: Permissions payload missing')
        if permission not in payload['permissions']:
            abort(403, description='Forbidden: Not enough permissions')
        return True

    @staticmethod
    def verify_decode_jwt(token):
        AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
        API_AUDIENCE = os.environ.get('API_AUDIENCE')
        ALGORITHMS = os.environ.get('ALGORITHMS')
        try:
            jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
            jwks = json.loads(jsonurl.read())
            unverified_header = jwt.get_unverified_header(token)
            rsa_key = {}
            for key in jwks['keys']:
                if key['kid'] == unverified_header['kid']:
                    rsa_key = {
                        'kty': key['kty'],
                        'kid': key['kid'],
                        'use': key['use'],
                        'n': key['n'],
                        'e': key['e']
                    }
            if rsa_key:
                try:
                    payload = jwt.decode(
                        token,
                        rsa_key,
                        algorithms=ALGORITHMS,
                        audience=API_AUDIENCE,
                        issuer=f'https://{AUTH0_DOMAIN}/'
                    )
                    return payload
                except jwt.ExpiredSignatureError:
                    abort(401, description='Unauthorized: JWT Token expired')
                except jwt.JWTClaimsError:
                    abort(401, description='Unauthorized: JWT Incorrect '
                                           'claims, please check')
        except Exception:
            abort(401, description='Unauthorized: JWT cannot parse token')
        abort(401, description='Unauthorized: JWT unable to find kid key')


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = Auth.get_token_auth_header()
            payload = Auth.verify_decode_jwt(token)
            if Auth.check_permissions(permission, payload):
                _request_ctx_stack.top.current_user = payload
                return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
