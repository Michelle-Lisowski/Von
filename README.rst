.. image:: https://i.imgur.com/tidfPif.jpg
==========================================

.. image:: https://discordbots.org/api/widget/status/477014316063784961.svg?noavatar=true
   :target: https://discordbots.org/bot/477014316063784961
.. image:: https://discordbots.org/api/widget/lib/477014316063784961.svg?noavatar=true
   :target: https://discordbots.org/bot/477014316063784961

Procbot is a music, levelling and moderation bot for Discord written in Python.

This bot is offline quite often, so if you want to host it yourself, you are welcome to do so.

Usage
-----

To add Procbot to your own server, click on `this link <https://discordapp.com/api/oauth2/authorize?client_id=477014316063784961&permissions=8&scope=bot>`_.

Installing
----------

To install Procbot for self-hosting, you can simply click ``Clone or download`` followed by ``Download ZIP``.

Otherwise, you can clone the repository using Git:

.. code:: sh

    $ git clone https://github.com/sirtezza451/Procbot

To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/sirtezza451/Procbot
    $ cd Procbot
    $ git pull . development

Bot Initialisation
------------------

Once you have installed Procbot on your computer, you will need to create the JSON files required
for specific functions. The following files must be created:

.. code::

    guilds.json
    mod_logs.json
    xp.json

Each of these must contain an empty dictionary:

.. code::

    {}

Once you have prepared the necessary files, you will need to get a bot token
by creating an app `here <https://discordapp.com/developers/applications>`_.
Copy that token and run ``setup.py``. Paste your token in when asked, and it
will save it in ``settings.json``. The bot will then be run automatically.

As the owner, you can log the bot out of Discord any time using the ``.logout`` command. After the first time setup,
you can run ``setup.py`` and choose from these three options without needing your token:

* Run Procbot
* Update Procbot from ``master`` branch
* Update Procbot from ``development`` branch

The second option will pull the code from the ``master`` branch, and you'll need to setup your token again.
The third option does the same, but for the ``development`` branch.

The last two options require `Git <https://git-scm.com/>`_ to function properly.

Note that when running your own instance of Procbot, you will also need your own server invite link.

Requirements
------------

* Python 3.6.x (voice breaks with 3.7)
* ``discord`` library (`GitHub repository <https://github.com/Rapptz/discord.py/tree/rewrite>`_; **rewrite** branch required)
* ``youtube_dl`` library (`GitHub repository <https://github.com/rg3/youtube-dl>`_)
* Bot token from Discord
* `Git <https://git-scm.com/>`_ (optional)
