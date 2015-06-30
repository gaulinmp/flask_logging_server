# -*- coding: utf-8 -*-
import os
import logging

from flask import Flask, request, render_template
from flask_wtf.csrf import CsrfProtect

from .controllers import logger, user
from .extensions import all_extensions, db


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    CsrfProtect(app)

    # Register extensions
    for ext in all_extensions:
        print(ext)
        ext.init_app(app)
    # Add DB resource to app object for use later.
    app.db = db

    # Creates DB if it doesn't exist. Comment out to avoid checking every time.
    if not os.path.exists(app.config['DBFILE_PATH']):
        print("Need to create {} at {}".format(app.config['DB_NAME'],
                                               app.config['APP_DIR']))
        @app.before_first_request
        def initialize_database():
            print("Creating {} at {}".format(app.config['DB_NAME'],
                                             app.config['APP_DIR']))
            db.create_all()
            from baseapp.controllers.user.models import User
            user = User(username='admin',
                        email='gaulinmp@gmail.com',
                        password='admin',
                        active=True,
                        admin=True)
            user.save()
            from baseapp.controllers.logger.models import LogProject
            p = LogProject(id=0, name="Default")
            p.save()

    # Register blueprints
    app.register_blueprint(logger.views.blueprint)
    logger.views.blueprint.extra_init(app)
    app.register_blueprint(user.views.blueprint)

    app.logger.setLevel(logging.WARNING)

    register_errorhandlers(app)

    return app

# From @sloria/cookiecutter-flask
def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("errors/{0}.html".format(error_code)), error_code
    for errcode in [404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
