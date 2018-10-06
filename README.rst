.. image:: https://i.imgur.com/YBCXiog.jpg
==========================================

.. image:: https://discordbots.org/api/widget/status/477014316063784961.svg?noavatar=true
   :target: https://discordbots.org/bot/477014316063784961
.. image:: https://discordbots.org/api/widget/lib/477014316063784961.svg?noavatar=true
   :target: https://discordbots.org/bot/477014316063784961

Jaffa is a music, levelling and moderation bot for Discord written in Python.

This bot is offline quite often, so if you want to host your own instance, you are welcome to do so.

Usage
-----

To add Jaffa to your own server, click on `this link <https://discordapp.com/api/oauth2/authorize?client_id=477014316063784961&permissions=8&scope=bot>`_.

Installing
----------

To install Jaffa for self-hosting, you can simply click ``Clone or download`` followed by ``Download ZIP``.

Otherwise, you can clone the repository using Git:

.. code:: sh

    $ git clone https://github.com/sirtezza451/Jaffa.git
    $ cd Jaffa

To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/sirtezza451/Jaffa.git
    $ cd Jaffa
    $ git checkout development
    $ git pull

Bot Initialisation
------------------

Once you have installed Jaffa on your computer, you will need to create the JSON files required
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

After the first time setup, you can run ``setup.py`` and choose from these
four options without needing your token:

* Run Jaffa
* Pull code from ``master`` branch
* Pull code from ``development`` branch
* Update requirements

The second option will pull the code from the ``master`` branch, and you'll need to setup your token again.
The third option does the same, but for the ``development`` branch.

The update-related options require `Git <https://git-scm.com/>`_ to function properly.

Note that when running your own instance of Jaffa, you will also need your own server invite link.

Owner Commands
--------------

As the owner of your own instance of Jaffa, only you can use the following commands:

.. code::

    .logout
    .load
    .unload
    .reload

``.logout`` logs the bot out from Discord.

``.load <extension>`` loads a specific extension, for example: ``.load ext.admin``

``.unload <extension>`` unloads a specific extension, for example: ``.unload ext.admin``

``.reload <extension>`` reloads a specific extension, for example: ``.reload ext.admin``

Requirements
------------

* `Python 3.6.x <https://www.python.org/search/?q=3.6&submit=>`_; voice functionality breaks with Python 3.7
* ``discord`` library (`GitHub repository <https://github.com/Rapptz/discord.py/tree/rewrite>`_; **rewrite** branch required)
* ``youtube_dl`` library (`GitHub repository <https://github.com/rg3/youtube-dl>`_)
* Bot token from `Discord <https://discordapp.com/developers/applications/@me>`_
* `Git <https://git-scm.com/>`_ (optional)
