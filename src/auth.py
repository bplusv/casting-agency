from functools import wraps
import json
import enum

from flask import Blueprint, request, jsonify, _request_ctx_stack
from urllib.request import urlopen
from jose import jwt


bp = Blueprint('auth', __name__)

AUTH0_DOMAIN = 'fs-capstone.us.auth0.com'
API_AUDIENCE = 'https://fs-capstone.herokuapp.com/api'
ALGORITHMS = ["RS256"]


class Role(enum.Enum):
    CASTING_ASSISTANT = 1
    CASTING_DIRECTOR = 2
    EXECUTIVE_PRODUCER = 3


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


class Auth:
    @staticmethod
    def get_token_auth_header():
        auth = request.headers.get("Authorization", None)
        if not auth:
            raise AuthError({"code": "authorization_header_missing",
                            "description":
                                "Authorization header is expected"}, 401)
        parts = auth.split()
        if parts[0].lower() != "bearer":
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Authorization header must start with"
                                " Bearer"}, 401)
        elif len(parts) == 1:
            raise AuthError({"code": "invalid_header",
                            "description": "Token not found"}, 401)
        elif len(parts) > 2:
            raise AuthError({"code": "invalid_header",
                            "description":
                                "Authorization header must be"
                                " Bearer token"}, 401)
        token = parts[1]
        return token

    @staticmethod
    def check_permissions(permission, payload):
        if 'permissions' not in payload:
            raise AuthError({
                'code': 'permissions_payload_missing',
                'description': 'Permissions payload missing.'
            }, 401)
        if permission not in payload['permissions']:
            raise AuthError({
                'code': 'not_authorized',
                'description': 'Not authorized'
            }, 401)
        return True

    @staticmethod
    def verify_decode_jwt(token):
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
                return payload
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                "description": "Token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                "description":
                                    "Incorrect claims, please check the"
                                    "audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                "description":
                                    "Unable to parse authentication"
                                    " token."}, 401)
        raise AuthError({"code": "invalid_header",
                        "description": "Unable to find appropriate key"}, 401)


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
