Taask
=====

**A future-proof, customisable task organiser.**

.. image:: http://www.taask.org/images/taask_screenshot.png
   :alt: Taask screenshot

|

===========================  ===============================
**Development started**      Sept 2014
**Stable version expected**  Dec 2014 / Jan 2015
**Working demo**             `taask.org <http://taask.org>`_
===========================  ===============================

Contents
--------

`1. The problems Taask solves
<https://github.com/countermeasure/taask#1-the-problems-taask-solves>`_

`2. Help build Taask
<https://github.com/countermeasure/taask#2-help-build-taask>`_

`3. Acknowledgments
<https://github.com/countermeasure/taask#3-acknowledgments>`_

`4. Setting up a development instance
<https://github.com/countermeasure/taask#4-setting-up-a-development-instance>`_


1. The problems Taask solves
----------------------------

1.1 Escaping from data prison
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Task management software usually likes to store your data in a proprietary
format in a database. This makes moving from one task management system to
another difficult if you ever want to.

Taask is built on top of the excellent command-line task manager
`Taskwarrior <http://taskwarrior.org>`_. Taskwarrior stores all your data in
human-readable YAML-esque text files. No database!

1.2 Future proofing your data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Data formats change over time. A proprietary data format that works today may be
impossible to work with in 20 years time.

With Taask and Taskwarrior, your data will continue to be accessible for as long
as computers can read text files.

Also, as text files, your data can be version controlled if you're so inclined.

1.3 Configurability
^^^^^^^^^^^^^^^^^^^

Task management software is usually hard or impossible to customise beyond the
built-in configuration settings. Need extra fields or custom logic? No go!
You're expected to make your workflow fit your software.

Because Taask is built using `Django <https://www.djangoproject.com>`_, it's
easy to modify or extend. Mould it to your workflow and make it operate just the
way you want!

1.4 Long term support
^^^^^^^^^^^^^^^^^^^^^

The task manager you use today may not be maintained, or may not even exist, in
5 or 10 years time.

I rely heavily on my task manager, and I'm building Taask to be my permanent
"daily driver". I'll be using and maintaining Taask for the next 50 years, if I
live that long!


2. Help build Taask
--------------------

Check the `Issue tracker <https://github.com/countermeasure/taask/issues>`_ for
work which needs to be done.

I'm kind of hoping that someone smarter than me can implement sub-tasks. Could
you be that person?


3. Acknowledgments
------------------

These projects make Taask possible:

`Taskwarrior <http://taskwarrior.org>`_: The command line task management tool
which is the brains of Taask

`Django <https://www.djangoproject.com>`_: The Python web-app framework which
Taask's front-end is built with

`Taskw <https://github.com/ralphbean/taskw>`_: A Python API which lets Django
talk to Taskwarrior

`Tablesorter <https://mottie.github.io/tablesorter>`_: A jQuery library which
sorts and filters tables

`jQuery/jQueryUI <https://jquery.com>`_: Javascript libraries

`Bootstrap <http://getbootstrap.com>`_: Styling framework

`Fontawesome <http://fontawesome.io>`_: Icons


4. Setting up a development instance
------------------------------------

Work on Taask started on 30 September 2014, and it isn't stable yet, so don't
even think about relying on it at the moment!

If you'd like contribute to the project, the steps below will guide you through
setting up a development instance.

Don't forget though, that if you just want to get a quick feel for Taask,
there's a demo at `taask.org <http://taask.org>`_ that you can test-drive!

4.1 Install Taskwarrior
^^^^^^^^^^^^^^^^^^^^^^^

::

    sudo apt-get install task

4.2 Install pip, virtualenv and virtualenvwrapper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may already have these installed. If so, skip this step.

::

    sudo apt-get install python-pip
    sudo pip install virtualenv virtualenvwrapper

Add these lines to the end of your ``~/.bashrc`` file:

::

    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/Projects
    source /usr/local/bin/virtualenvwrapper.sh

Reload ``~/.bashrc``:

::

    source ~/.bashrc

4.3 Set up a virtualenv
^^^^^^^^^^^^^^^^^^^^^^^

::

    mkvirtualenv taask

Add these lines to the end of ``~/.virtualenvs/taask/bin/postactivate``:

::

    export TAASK_ENVIRONMENT=development
    export TAASK_SECRET_KEY=njf7hd9j356dgfekf9rehn43fre89uy3g
    export TAASK_STATIC_ROOT=not_used_for_local_instances

Restart the virtualenv so that these setting take effect:

::

    deactivate
    workon taask

4.4 Clone the repo
^^^^^^^^^^^^^^^^^^

For these instructions we'll clone the repo to ``~/Projects``, but you can put
it anywhere you like.

::

    mkdir ~/Projects
    cd ~/Projects
    git clone https://github.com/countermeasure/taask.git

4.5 Install dependencies
^^^^^^^^^^^^^^^^^^^^^^^^

::

    cd ~/Projects/taask
    pip install -r requirements.txt

4.6 Configure
^^^^^^^^^^^^^

::

    cp ~/Projects/taask/configuration/.taskrc ~
    cp -r ~/Projects/taask/fixtures/.task ~

4.7 Start the server
^^^^^^^^^^^^^^^^^^^^

::

    python manage.py runserver

4.8 Open Taask
^^^^^^^^^^^^^^

Browse to ``localhost:8000/list-tasks/today``.
