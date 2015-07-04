"""
Example logger file.

I've found this doesn't work on bluehost, unless you set up the handler thus:

http_handler = logging.handlers.HTTPHandler(
    'example.com',
    'http://example.com/path_to_logger/api_upload?key=test&other_keys...',
    method='GET',
)
"""

import logging
import logging.handlers
logger = logging.getLogger()
http_handler = logging.handlers.HTTPHandler(
    'localhost:5000',
    '/api_upload?key=test&project_id=0&submitter=me&email_to=me@example.com',
    method='GET',
)
http_handler.setLevel(logging.DEBUG) # probably not a good idea...
logger.addHandler(http_handler)
logger.debug('Test of debug level.')
logger.info('Test of info level.')
logger.warning('Test of warning level.')
logger.error('Test of error level.')
logger.critical('Test of critical level.')
