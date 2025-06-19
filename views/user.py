from flask import Flask, render_template, request, flash, session, redirect, url_for, Blueprint

import forms
from service.user_service import UserService


user_bp = Blueprint('user', __name__)


@user_bp.route('/signin', methods=['GET', 'POST'])
def view_signin_page():
    form = forms.SignInForm(request.form)

    if request.method == 'POST':
        user = UserService.verify(
            request.form['login'],
            request.form['password']
        )
        if not user:
            flash("Špatné přihlašovací údaje.", 'error')
        else:
            session['authenticated'] = 1
            session['user_id'] = user['id_uzivatele']
            session['email'] = user['email']
            session['role'] = user['nazev_role']
            session['role_id'] = user['id_role']
            return redirect(url_for('home_page.page'))

    return render_template("auth/sign_in/page.jinja", form=form, no_header=True)


@user_bp.route('/register', methods=['GET', 'POST'])
def view_register_page():
    form = forms.RegisterForm(request.form)

    if request.method == 'POST':
        error = UserService.register(
            login = request.form['login'],
            password = request.form['password'],
            confirm_password = request.form['confirm_password'],
            first_name = request.form['first_name'],
            last_name = request.form['last_name'],
        )
        if error:
            flash(error, 'error')
            return redirect(url_for('user.view_register_page'))
        else:
            flash("Registrace byla úspěšná.", 'success')
            return redirect(url_for('user.view_signin_page'))

    return render_template("auth/register/page.jinja", form=form, no_header=True)


@user_bp.route('/signout')
def signout():
    session.pop('authenticated')
    session.pop('user_id')
    session.pop('role')
    flash("Odhlášení proběhlo úspěšně.", 'success')
    return redirect(url_for('home_page.page'))