from flask import session, redirect, url_for
from functools import wraps


def is_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        name = session.get('name', '')
        if name:
            return func(*args, *kwargs)
        else:
            return redirect(url_for('login.login'))
    return wrapper
