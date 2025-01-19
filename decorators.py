from functools import wraps
from flask import g, url_for, redirect
from datetime import datetime

# def logger(func):
#     f = open("static/logger/log.txt", "a", encoding="utf-8")
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         f.write(f" - 开始:")
#         return func(*args, **kwargs)
#     f.close()
#     return wrapper


# @logger
def login_required(func):
    @wraps(func)  # 先保留存入函数的代码和功能
    def inner(*args, **kwargs):
        if g.user:   # 如果用户存在 则正常返回func 应该执行的代码
            return func(*args, **kwargs)
        else:  # 如果用户不存在，则不能正常访问页面，重定向到登录界面
            return redirect(url_for('auth.login'))
    return inner

