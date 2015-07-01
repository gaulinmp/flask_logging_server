# -*- coding: utf-8 -*-
import logging
try:
        from urllib.parse import urlparse, urljoin
except ImportError:
        from urlparse import urlparse, urljoin

from flask import request, url_for, redirect, flash

def flash_errors(form, category=None):
    """ Call `flash` on every error in form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash("{} - {}".format(getattr(form, field).label.text, error),
                  category if category else 'warning')

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
