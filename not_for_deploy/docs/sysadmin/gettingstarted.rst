###############
Getting started
###############


********************************
Install required system packages
********************************

#. Python 2.7.X. Check your current version by running ``python --version``.
#. PIP_
#. VirtualEnv_
#. PostgreSQL server. Alternatively, you can test out Devilry with SQLite,
   but you will need PostgreSQL for production.


********************************
Create a system user for Devilry
********************************
You should run Devilry as a non-privledged user. We suggest you name the user
something like ``devilryrunner``. **Run all commands in this documentation as
this user unless stated otherwise**.


****************************************
Make a directory for your Devilry deploy
****************************************
You need a directory for your Devilry settings and other Devilry-related files.
We suggest you use the ``~/devilrydeploy/`` directory (in the HOME folder of
the ``devilryrunner``-user)::

    $ mkdir ~/devilrydeploy

The rest of the guide will assume you use the ``~/devilrydeploy``-directory


********************************************
Make a requirements file for Python packages
********************************************
To run Devilry in production, you need the Devilry library, and a couple
of extra Python packages and perhaps you will want to install some third
party devilry addons. We could just install these, but that would be
messy to maintain. Instead, we use a PIP requirements-file. Create
``~/devilrydeploy/requirements.txt`` with the following contents::

    # PostgreSQL python bindings
    psycopg2

    # Supervisord process manager
    supervisor

    # The devilry library/djangoproject
    # - See http://devilry.org for the latest devilry version
    devilry==VERSION

Where ``VERSION`` should be set to the latest version of Devilry.


**********************************
Install from the requirements file
**********************************
::

    $ cd ~/devilrydeploy
    $ virtualenv venv
    $ venv/bin/pip install -r requirements.txt


*********************************
Create a Django management script
*********************************
Copy this script into ``~/devilrydeploy/manage.py``::

    import os
    import sys

    if __name__ == "__main__":
        os.environ["DJANGO_SETTINGS_MODULE"] = "devilry_settings"
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)



*********
Configure
*********
Devilry is configured through a python file. We will start by configuring the
essential parts to get a working Devilry server, and then move on to
guides for the more complex parts like search and authentication in
separate chapters.

Start by copying the following into ``~/devilrydeploy/devilry_settings.py``::

    from devilry.project.production.settings import *
    import dj_database_url
    from devilry.utils import rq_setup

    # Make this 50 chars and RANDOM - do not share it with anyone
    SECRET_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

    # Database config
    DATABASE_URL = 'sqlite:///devilrydb.sqlite'
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL)}

    # Set this to False to turn of debug mode in production
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    #: Default from email - students receive emails from this address when they make deliveries
    DEVILRY_EMAIL_DEFAULT_FROM = 'devilry-support@example.com'

    #: The URL that is used to link back to devilry from emails
    DEVILRY_SCHEME_AND_DOMAIN = 'https://devilry.example.com'

    #: Where should Devilry store files delivered by students.
    #: This directory should be backed up.
    DEVILRY_FSHIERDELIVERYSTORE_ROOT = '/path/to/directory/for/deliveryfiles/'

    #: The directory where user uploaded files such as attachments to feedback is uploaded.
    #: This directory should be backed up.
    MEDIA_ROOT = '/path/to/directory/for/uploadedfiles/'

    #: The directory where compressed archives are stored. Archives are compressed when examiners or students
    #: downloads files from an assignment or a feedbackset.
    #: See the ``Compressed archives for filedownload`` guide.
    DEVILRY_COMPRESSED_ARCHIVES_DIRECTORY = '/path/to/directory/for/compressedarchives/'

    #: Url where users are directed when they do not have the permissions they believe they should have.
    DEVILRY_LACKING_PERMISSIONS_URL = None

    #: Url where users are directed when they want to know what to do if their personal info in Devilry is wrong.
    DEVILRY_WRONG_USERINFO_URL = None

    #: Url where users can go to get documentation for Devilry that your organization provides.
    #: If you leave this blank, the only help link will be the official Devilry documentation.
    DEVILRY_ORGANIZATION_SPECIFIC_DOCUMENTATION_URL = None

    #: Text for the DEVILRY_ORGANIZATION_SPECIFIC_DOCUMENTATION_URL link.
    #: Leave this blank to use the default text
    DEVILRY_ORGANIZATION_SPECIFIC_DOCUMENTATION_TEXT = None

    #: Deadline handling method:
    #:
    #:    0: Soft deadlines
    #:    1: Hard deadlines
    DEFAULT_DEADLINE_HANDLING_METHOD = 0

    #: Can students edit their comments?
    DEVILRY_COMMENT_STUDENTS_CAN_EDIT = True

    #: Should students be able to see the comment edit history of other users in their group?
    #: If this is set to `False`, students can still see that the comment has been edited, but not the edit history.
    DEVILRY_COMMENT_STUDENTS_CAN_SEE_OTHER_USERS_COMMENT_HISTORY = True

    #: Configure an email backend.
    #: See https://docs.djangoproject.com/en/2.0/ref/settings/ for details about these settings.
    #: If you have performance issues with your email backend, see ``Sending emails in background task``.
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 25
    EMAIL_USE_TLS = False

    #: Setup Redis connection settings for background task server.
    #: For a complete custom setup, see the ``Setup Redis with RQ for background task processing``
    #: section of the docs for details about this setting.
    RQ_QUEUES = rq_setup.make_simple_rq_queue_setting(
        host='localhost',
        port=6379,
        db=0,
        password='secret'
    )


If you have a ``devilry_prod_settings.py`` file from an older version of Devilry, you should be
able to copy over most of these settings.


Make sure it works
==================
Just to make sure everything works, run::

    $ cd ~/devilrydeploy/
    $ venv/bin/python manage.py syncdb --noinput
    $ venv/bin/python manage.py migrate --noinput

This should create a file named ``~/devilrydeploy/devilrydb.sqlite``.
You can remove that file now - it was just for testing.


Configure a SECRET_KEY
======================
Configure the SECRET_KEY (used for cryptographic signing) by editing the ``SECRET_KEY`` setting in your
``devilry_settings.py`` script. Make it a 50 characters long random string.


Configure the database
======================
Configure a Postgres database by editing the ``DATABASE_URL`` setting in your ``devilry_settings.py`` script.
The format is::

    DATABASE_URL = "postgres://USER:PASSWORD@HOST:PORT/NAME"

.. note::

    If you are just testing out Devilry, you can keep SQLite as the database.


Configure where to store files
==============================
Adjust the ``DEVILRY_FSHIERDELIVERYSTORE_ROOT`` setting to a directory where you want delivered files
to be stored, and the ``MEDIA_ROOT`` setting to a directory where you want to place all other uploaded files,
such as files uploaded as attachments when examiners provide feedback.


Configure various external pages
================================
Make sure you create a website that you can link to for the ``DEVILRY_LACKING_PERMISSIONS_URL``
and ``DEVILRY_WRONG_USERINFO_URL`` pages. You may also want to configure a
``DEVILRY_ORGANIZATION_SPECIFIC_DOCUMENTATION_URL``, but that is not required.


Disable debug mode
==================
Before running Devilry in production, you **must** set ``DEBUG=False`` in ``devilry_settings.py``.

.. warning::

    If you do not disable DEBUG mode in production, you database credentials and SECRET_KEY
    will be shown to any visitor when they encounter an error.


****************************
Create or migrate a database
****************************
No matter if the current the database contains a database from a previous Devilry version,
or if you are starting from an empty database, you need to run::

    $ cd ~/devilrydeploy/
    $ venv/bin/python manage.py syncdb --noinput
    $ venv/bin/python manage.py migrate --noinput

This will create any missing database tables, and migrate any unmigrated database changes.



********************
Collect static files
********************
Run the following command to collect all static files (CSS, javascript, ...) for Devilry::

    $ cd ~/devilrydeploy/
    $ venv/bin/python manage.py collectstatic

The files are written to the ``staticfiles`` sub-directory (``~/devilrydeploy/staticfiles``).


***********************
Run the gunicorn server
***********************
Run::

    $ cd ~/devilrydeploy/
    $ DJANGO_SETTINGS_MODULE=devilry_settings venv/bin/gunicorn devilry.project.production.wsgi -b 0.0.0.0:8000 --workers=3 --preload

You can adjust the number of worker threads in the ``--workers`` argument,
and the port number in the ``-b`` argument.

.. note::

    This is not how you should run this in production. Below, you will learn how to setup
    SSL via a webserver proxy, and Supervisord for process management.



*********************************************************
If you do not have an existing database --- Add some data
*********************************************************
If you do not have a Devilry database from a previous version of Devilry,
you will want to add some data.

First, create a superuser::

    $ cd ~/devilrydeploy/
    $ venv/bin/python manage.py createsuperuser

Next:

- Go to http://localhost:8000/
- Login with your newly created superuser.
- Select the *Superuser* role.
- Add a **Node**. The toplevel node is typically the name of your school/university.
- Add a **Course** within the created node. Make sure you make yourself admin on the course.
- Go back to http://localhost:8000/. You should now have a new *Course manager* role available
  on the frontpage.


********************************
If you have an existing database
********************************
If you already have a working Devilry database, you will most likely have to configure
and authentication backend before you can do any more testing (explained below).


************************
Stop the gunicorn server
************************
When you are done testing, stop the gunicorn server (with ``ctrl-c``), and move on to
setting up the more complex parts of the system.


***********
Whats next?
***********
You now have a working Devilry server, but you still need to:

- :doc:`authbackend`.
- :doc:`supervisord`.
- :doc:`webserver`.


.. _PIP: https://pip.pypa.io
.. _VirtualEnv: https://virtualenv.pypa.io
