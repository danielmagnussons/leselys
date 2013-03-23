Leselys
=======

I'm Leselys, your very elegant RSS reader.

No `bullshit apps`_ for Android, iPhone, etc. Just a responsive design and for every device.

Leselys is Heroku ready. There is a `demo here`_ (demo/demo).

Installation
------------

Ubuntu
~~~~~~

Two requirements: **Mongodb** and **Python**.

In order to install leselys you'll need some dependencies: ::

	apt-get install build-essential python-dev python-pip
	apt-get install libxslt1-dev libxml2-dev python-libxml2 python-libxslt1

And install your `Mongodb`_.

.. _Mongodb: http://docs.mongodb.org/manual/installation/

::

	pip install leselys
	leselys init leselys.ini
	leselys adduser leselys.ini
	leselys serve leselys.ini
	# In another terminal
	leselys worker leselys.ini

Open your browser at ``http://localhost:5000``.


Heroku
~~~~~~

Advanced setup with MongoDB for storage and Redis for session on Heroku.
You will also need the Heroku Scheduler add-on to refresh your feeds.

All Heroku dependencies like ``Pymongo``, ``gunicorn`` and ``redis`` are in ``requirements-heroku.txt`` file.

::

	git clone git@github.com:socketubs/leselys.git
	cd leselys
	cp requirements-heroku.txt requirements.txt
	heroku create
	heroku addons:add mongohq:sandbox
	heroku addons:add redistogo:nano
	heroku addons:add scheduler:standard
	heroku addons:open scheduler
	# Add "sh heroku.sh && leselys refresh heroku.ini" job
	git push heroku master

Don't forget to create a Leselys account with ``heroku run "bash heroku.sh && leselys adduser --config heroku.ini"``.

Import your Google Reader OPML file right now!

Misc
----

Storage and session backends are Python modules, you can easily write your own. Take a look at the `MongoDB`_ storage backend.

License
-------

License is `AGPL3`_. See `LICENSE`_.

.. _bullshit apps: http://tommorris.org/posts/8070
.. _demo here: https://leselys.herokuapp.com
.. _MongoDB: https://github.com/socketubs/leselys/blob/master/leselys/backends/_mongodb.py
.. _Ubuntu: https://github.com/socketubs/leselys/wiki/Ubuntu
.. _Heroku: https://github.com/socketubs/leselys/wiki/Heroku
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _LICENSE: https://raw.github.com/socketubs/leselys/master/LICENSE
