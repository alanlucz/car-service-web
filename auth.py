from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from functools import wraps

def login_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Musíte se nejdříve přihlásit.', 'warning')
            return redirect(url_for('user.view_signin_page'))
        return function(*args, **kwargs)
    return decorated_function

def roles_required(*roles):
    def roles_decorator(function):
        @wraps(function)
        def decorated_function(*args, **kwargs):
            if session['role'] not in roles:
                flash('Pro tuto akci nemáte oprávnění.', 'error')
                return redirect(url_for('home_page.page'))
            return function(*args, **kwargs)
        return decorated_function
    return roles_decorator