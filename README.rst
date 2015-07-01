================================
Flask Boilerplate
================================

Empty Flask app with default User login working.

Quick Start
------------
#. Clone the repo, or run code similar to `this gist <https://gist.github.com/gaulinmp/c558a8cc9192eeda316d#file-new_flask_from_mold-sh>`_.

#. Check out sqlalchemy branch if that's your cup of tea (`git pull source sqlalchemy`)

   #. If using sqlalchemy, run the server once to automatically create the DB.

#. Add pages by:

   #. copying the controllers.user or pages.py from baseapp, then adding new blueprint to loading.

   #. Adding to pages.py in baseapp.controllers.


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

.. image:: https://raw.githubusercontent.com/gaulinmp/flask_mold/master/home.png
   :scale: 25 %
   :alt: Plain bootstrap white theme.
   :align: center
