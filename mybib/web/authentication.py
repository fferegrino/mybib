import os
from functools import wraps

from flask import Response, request


def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    mybib_user = os.getenv("MYBIB_USER")
    mybib_pass = os.getenv("MYBIB_PASSWORD")
    if mybib_pass and mybib_user:
        return username == mybib_user and password == mybib_pass
    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        "Could not verify your access level for that URL.\n"
        "You have to login with proper credentials",
        401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
