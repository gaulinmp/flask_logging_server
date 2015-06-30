# -*- coding: utf-8 -*-
from datetime import timedelta

from flask import request, url_for, redirect, session, current_app
from flask_wtf import Form
from wtforms import StringField, IntegerField, SelectField, HiddenField
from wtforms.validators import DataRequired, Length
from wtforms.csrf.session import SessionCSRF
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .models import LogEntry, LogProject, get_log_level, LEVELS_INVERSE
from ...utilities import get_redirect_target, is_safe_url

class RedirectForm(Form):
    nextpage = HiddenField()

    def __init__(self, *args, **kwargs):
        super(RedirectForm, self).__init__(*args, **kwargs)
        if not self.nextpage.data:
            self.nextpage.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.nextpage.data):
            return redirect(self.nextpage.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))


class ProjectCreateForm(RedirectForm):
    name = StringField(
        'Project Name', validators=[DataRequired(), Length(min=1, max=31)]
    )

    def __init__(self, *args, **kwargs):
        super(ProjectCreateForm, self).__init__(*args, **kwargs)


class LogEntryForm(RedirectForm):
    project_id = SelectField('Project ID', choices=[(0, 'Default')], coerce=int)
    email_to = StringField('Email To')
    submitter = StringField('Submitted By')
    message = StringField('Message', [DataRequired()])
    level = SelectField('Log Level', coerce=int,
                        choices=sorted(LEVELS_INVERSE.items()))

    def __init__(self, *args, **kwargs):
        print(args)
        print(kwargs)
        print("That was the form")
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        initial_validation = super(LogEntryForm, self).validate()
        if not initial_validation:
            for k,v in self.__dict__.items():
                try: print(k, v.data)
                except: pass
            print(self.errors)
            print("Didn't pass muster.")
            return False

        project = LogProject.query.filter_by(id=self.project_id.data).first()
        if not project:
            self.project_id.data = 0

        self.level.data = get_log_level(self.level.data)

        return True
