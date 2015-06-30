# -*- coding: utf-8 -*-
from flask import (Blueprint, render_template, request, flash,
                   session, redirect, url_for)
from flask.ext.login import login_user, login_required, logout_user, current_user

from .forms import LoginForm, ForgotForm, RegisterForm
from .models import User
from ...utilities import flash_errors
from ...extensions import login_manager

blueprint = Blueprint('user', __name__, url_prefix='/user',
                      static_folder='../static',
                      template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    uuser = User.search(user_id=int(user_id))
    return uuser

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('user.login'))

################################################################################
####           Routes                                                       ####
################################################################################

@blueprint.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash_errors(form)
            return render_template("login.html", form=form)
        # user password validation done in WTForm
        login_user(form.user)
        form.user.authenticate(is_authentic=True)
        flash("You are logged in.", 'success')
        session['user_id'] = form.user.id
        return form.redirect(url_for('user.login'))

    return render_template("login.html", form=form)


@blueprint.route('/logout')
@login_required
def logout():
    current_user.authenticate(is_authentic=False)
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('baseapp.home'))


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        new_user = User.create(username=form.username.data,
                               email=form.email.data,
                               password=form.password.data,
                               active=False) # Gotta be confirmed.
        flash('Thanks for registering. You may be confirmed later.', 'success')
        return redirect(url_for('baseapp.home'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forgot.html', form=form)
