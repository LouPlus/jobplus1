#装饰器

from flask import abort
from flask_login import current_user
from functools import wraps
from jobplus.models import User

def role_required(role):

    def decorators(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role < role:
                abort(404)
            return func(*args, **kwargs)
        return wrapper
    return decorators

employee_required = role_required(User.ROLE_EMPLOYEE)
company_required = role_required(User.ROLE_COMPANY)
admin_required = role_required(User.ROLE_ADMIN)