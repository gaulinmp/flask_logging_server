#!/home1/USERNAME/python/2.7/bin/python
# ^^ This is a custom install of python, change it to reflect your server ^^

# put this file in public_html root, like ~/public_html/flask/log
# below, set APPLICATION_ROOT to this file, including filename (here ``log``)

import os
import sys
sys.path.insert(0, '/home1/USERNAME/projects/flask_logging_server/')
os.environ['LOGGING_UPLOAD_KEY'] = 'whatever you want the &key=BLAH thing to be'
os.environ['SECRET_KEY'] = 'make me super secret yo'

from flup.server.fcgi import WSGIServer
# Change this line to run new app
from baseapp import create_app

from config.default_server import ProdConfig as config

config.APPLICATION_ROOT = '/projects/log/' # <-- set this to this file path (see above)

app = create_app(config)

if __name__ == '__main__':
    WSGIServer(app).run()
