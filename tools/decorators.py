from flask import session, redirect, url_for
from functools import wraps


# 定义登录装饰器，判断用户是否登录
def is_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 判断session是否保存了用户名，保存了即该用户已登录
        name = session.get('name', '')
        if name:
            return func(*args, *kwargs)
        else:
            # 未登录重定向到登录页面
            return redirect(url_for('login.login'))
    return wrapper
