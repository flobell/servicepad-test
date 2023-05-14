import logging
from flask import current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_caching import Cache
from werkzeug.exceptions import BadRequest, Unauthorized, NotFound
from functools import wraps
from http import HTTPStatus


def http_exceptions_handler(f):
    """
        decorator for handling exception on https requests
        generally for setting an standart output at an 
        internal server error, also prints in logs.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
            response=dict(
                message=str(e)
            )
            return response, int(HTTPStatus.INTERNAL_SERVER_ERROR)
    return wrapper


def jwt_required(fn):
    """
        Custom jwr_required decorator to verify the jwt in the request
        and check blacklisted jwt by logout.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()  # Verify the JWT in the request

        jti = get_jwt()["jti"]

        # Check if the jti is blacklisted in the cache
        blacklisted = current_app.cache.get(jti)
        if blacklisted:
            return dict({"message": "Invalid token"}), 401

        return fn(*args, **kwargs)

    return wrapper
