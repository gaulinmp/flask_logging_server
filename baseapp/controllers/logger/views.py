# -*- coding: utf-8 -*-
import json
import logging

from flask import (Blueprint, render_template, request, flash,
                   session, redirect, url_for, current_app)
from flask.ext.login import login_required, current_user

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

@blueprint.route("/", methods=["GET"]) # @login_required
def home():
    try:
        pid = int(request.args.get('project', -1))
    except ValueError:
        pid = -1
    level = request.args.get('level', logging.DEBUG)
    logs = LogEntry.search(project_id=pid, level=level
                          ).order_by('timestamp desc')[:25]
    projs = LogProject.query.order_by('id desc')
    numlogs = LogEntry.search(project_id=pid).count()
    return render_template("all_logs.html", logs=logs, projects=projs,
                           numlogs=(len(logs), numlogs))

@blueprint.route("/newlog", methods=["GET", "POST"])
@login_required
def submit_log():
    form = LogEntryForm(request.form)
    #ps = LogProject.query.order_by('id')
    #form.project_id.choices = [(p.id, p.name) for p in ps]
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
@login_required
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

@blueprint.route("/api_upload", methods=["GET"])
def api_create():
    form = LogEntryForm(request.args, csrf_enabled=False)
    # Workaround to allow native use of HTTPHandler
    if 'level' not in request.args and 'levelname' in request.args:
        form.level.data = request.args['levelname']
    if not form.validate():
        return "{'success':false, 'message':'Invalid supplied data'}", 401

    upkey = current_app.config['LOGGING_UPLOAD_KEY']
    if len(upkey) < 1:
        return "{'success':false, 'message':'Auth config missing.'}", 500

    if upkey != request.args.get('key', ''):
        return "{'success':false, 'message':'Not authenticated.'}", 403

    l = LogEntry.create(submitter=form.submitter.data,
                        email_to=form.email_to.data,
                        project_id=form.project_id.data,
                        message=form.message.data,
                        level=form.level.data)

    return "{'success':true}", 200


@blueprint.route("/delete_old", methods=["GET"])
@login_required
def delete_old():
    MIN_KEEP = 25
    try:
        pid = int(request.args.get('project', -1))
    except ValueError:
        pid = -1
    logs = LogEntry.search(project_id=pid, level=0
                          ).order_by('timestamp desc')

    for i in range(logs.count() - MIN_KEEP, 0, -1): # i = COUNT - MIN_KEEP -> 0
        logs[-1].delete(commit=(i==1)) # Commit on last one (i==1)
    return redirect(url_for('baseapp.home'))


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
