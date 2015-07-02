import logging
import logging.handlers
logger = logging.getLogger()
http_handler = logging.handlers.HTTPHandler(
    'localhost:5000',
    '/api_upload?key=test&project_id=0&submitter=me&email_to=me@example.com',
    method='GET',
)
logger.addHandler(http_handler)
logger.debug('Test of debug level.')
logger.info('Test of info level.')
logger.warning('Test of warning level.')
logger.error('Test of error level.')
logger.critical('Test of critical level.')
