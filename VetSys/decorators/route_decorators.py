from functools import wraps
from flask_login import current_user
from VetSys import login_manager


def access_granted(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            user_type = current_user.user_type
            if role != user_type and role != "ANY":
                return "access restricted"
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper
