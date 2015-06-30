# -*- coding: utf-8 -*-
"""
Handles all LogEntry interaction.

Could have a database backend, or plaintext.
"""
import os
import json
import logging
import datetime as dt

from sqlalchemy.sql import and_, or_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from flask import current_app

from baseapp.extensions import bcrypt
from baseapp.database import (
    Column,
    db,
    Model,
    SurrogatePK,
)


LEVELS = {'critical':50, 'error':40, 'warning':30, 'info':20, 'debug':10}
LEVELS_INVERSE = {v:k.upper() for k,v in LEVELS.items()}  # add 10:debug

def get_log_level(int_or_string):
    level = logging.INFO
    try:  # Make sure 'level' is int
        level = int(int_or_string)
    except ValueError:  # value error means text (or other)
        txt = str(int_or_string).lower().strip()
        level = LEVELS.get(txt, level)
    return level

def get_str_level_from_int(int_level):
    level = get_log_level(int_level)  # Ensure int
    level = max(logging.DEBUG, min(logging.CRITICAL, level)) # coerce to 10..50
    level = level // 10 * 10  # Coerce to multiples of 10
    return LEVELS_INVERSE.get(level, 'INFO')  # default to INFO


class LogProject(SurrogatePK, Model):
    __tablename__ = 'log_projects'
    name = Column(db.String(80), nullable=False, default='default')

    def get_logs(self, min_level=logging.INFO):
        return LogEntry.search(project_id = self.id, level=min_level)

    def __repr__(self):
        return "<Project[{}]:'{}'>".format(self.id, self.name)

class LogEntry(SurrogatePK, Model):
    __tablename__ = 'log_entries'
    project_id = Column(db.ForeignKey("{}.id".format(LogProject.__tablename__)),
                        nullable=False, default=0)
    timestamp = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    submitter = Column(db.String(80), unique=False, nullable=True)
    email_to = Column(db.String(80), unique=False, nullable=True)
    message = Column(db.Text, nullable=True)
    level = Column(db.Integer, nullable=False, default=logging.INFO)

    project = relationship("LogProject", backref=backref('logs',
                                                         order_by=timestamp))

    LOG_FORMAT = ("{project_id}\t{level_name}\t"
                  "{timestamp:%Y-%m-%d %H:%M:%S}\t{message}")

    def __init__(self, **kwargs):
        try:
            level = get_log_level(kwargs['level'])
        except KeyError:
            level = logging.INFO
        kwargs['level'] = level

        if 'project_id' in kwargs:
            pids = set([x.id for x in LogProject.query.all()])
            if int(kwargs['project_id']) not in pids:
                kwargs['project_id'] = 0
        kwargs['project_id'] = int(kwargs['project_id'])
        
        db.Model.__init__(self, **kwargs)

    @hybrid_property
    def level_name(self):
        return get_str_level_from_int(self.level)

    def __repr__(self):
        return self.LOG_FORMAT.format(level_name=self.level_name, # TODO: fix
                                      **self.__dict__)

    @staticmethod
    def search(project_id=None, level=logging.INFO):
        """
        Searches `log_entry` database, returns log entries matching project_id
        and having at least `level` logging level.
        Leave project_id=None or project_id < 0 to get all.
        """
        q = LogEntry.query.filter(LogEntry.level>=get_log_level(level))

        if project_id is not None and project_id >= 0:
            q = q.filter(LogEntry.project_id==project_id)

        return q

    @staticmethod
    def create(**kwargs):
        """Factory method wrapping LogEntry(**kwargs)."""
        log = LogEntry(**kwargs)
        log.save()
        #print("Created LogEntry<{}>".format(log))
        return log
