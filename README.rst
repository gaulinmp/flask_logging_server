================================
Flask Logging Server
================================

Flask website for uploading and displaying logging messages from any web-connected computer.
Uses simple GET and a 'secret key' to upload.

Quick Start
------------
#) git clone https://github.com/gaulinmp/flask_logging_server.git to your server of choice (I use bluehost)
   
   #) Let's say you put it at ``$HOME/projects/flask_logging_server`` for now.

#) Put your WSGI run script in a folder somewhere in the ~/public_html folder.
   
   #) Let's say you put it at ``$HOME/public_html/projects/log`` for now.
   
   #) You could copy the ``example_wsgi.py`` script: ``cp example_wsgi.py $HOME/public_html/projects/log``

#) That's it for the server.

#) On any computer, send a GET request to the api_upload URI with the correct secret key

   #) ``http://``\ *YOURURL*\ ``/projects/log/api_upload?key=``\ *LOGGING_UPLOAD_KEY*\ ``&message=MY LOGGING MESSAGE``


Run
----------------
```sh
$ python run.py
```

Shell
-----------------
```sh
$ python shell.py
```

Screenshot
-----------------

.. image:: https://raw.githubusercontent.com/gaulinmp/flask_logging_server/master/home.png
   :scale: 25 %
   :alt: Plain bootstrap white theme.
   :align: center
