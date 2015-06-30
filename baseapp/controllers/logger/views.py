# -*- coding: utf-8 -*-
import json
import logging

from flask import (Blueprint, render_template, request, flash,
                   session, redirect, url_for)
from flask.ext.login import login_user, login_required, logout_user #, current_user

from .forms import LogEntryForm, ProjectCreateForm
from .models import LogEntry, LogProject
from ...utilities import flash_errors
from ...extensions import login_manager

blueprint = Blueprint('baseapp', __name__,
                      static_folder='../static',
                      template_folder='templates')


################################################################################
####           Routes                                                       ####
################################################################################

@blueprint.route("/", methods=["GET"])
def home():
    try:
        pid = int(request.args.get('project', -1))
    except ValueError:
        pid = -1
    level = request.args.get('level', logging.DEBUG)
    logs = LogEntry.search(project_id=pid, level=level
                          ).order_by('timestamp desc')[:25]
    projs = LogProject.query.order_by('id desc')
    return render_template("all_logs.html", logs=logs, projects=projs)

@blueprint.route("/newlog", methods=["GET", "POST"])
def submit_log():
    form = LogEntryForm(request.form)
    ps = LogProject.query.order_by('id')
    form.project_id.choices = [(p.id, p.name) for p in ps]
    # POST means submitting a log
    if request.method == 'POST':
        if form.validate_on_submit(): # create and redirect to home
            l = LogEntry.create(submitter=form.submitter.data,
                                email_to=form.email_to.data,
                                project_id=form.project_id.data,
                                message=form.message.data,
                                level=form.level.data)
            flash("Entry added! {}".format(l))
            return form.redirect(url_for('baseapp.home'))
        # else not valid. Flash errors and send them back to submission page.
        flash_errors(form)
    # GET means render the form
    return render_template("form.html", form=form, title="Submit Log")

@blueprint.route("/newproj", methods=["GET", "POST"])
def submit_project():
    form = ProjectCreateForm(request.form)
    # POST means submitting a log
    if request.method == 'POST':
        if form.validate_on_submit(): # create and redirect to home
            LogProject.create(name=form.name.data)
            return form.redirect(url_for('baseapp.home'))
        # else not valid. Flash errors and send them back to submission page.
        flash_errors(form)
    # GET means render the form
    return render_template("form.html", form=form, title="Submit Project")

@blueprint.route("/test", methods=["GET"])
def create_things():
    # for i in range(59):
    #     l = LogEntry.create(submitter='man {}'.format(i),
    #                         email_to='a{}@b.com'.format(i),
    #                         project_id=i%2,
    #                         message='Message {}'.format(i),
    #                         level=i)

    try:
        pid = int(request.args.get('project', -1))
    except ValueError:
        pid = -1
    logs = LogEntry.search(project_id=pid, level=logging.DEBUG
                          ).order_by('timestamp desc')
    projs = LogProject.query.all()
    return "{}\n{}".format(json.dumps([str(x) for x in logs]),
                           json.dumps([str(x) for x in projs]))


################################################################################
####           Add to App Context Manager                                   ####
################################################################################
def extra_init(app):
    """Extra blueprint initialization that requires application context."""
    if 'header_links' not in app.jinja_env.globals:
        app.jinja_env.globals['header_links'] = []
    # Add links to 'header_links' var in jinja globals. This allows header_links
    # to be read by all templates in the app instead of just this blueprint.
    #a = app.jinja_env.globals['header_links']
    #a.extend([("Home", 'baseapp.home')])
# Tack it on to blueprint for easy access in app's __init__.py
blueprint.extra_init = extra_init
