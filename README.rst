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

Once you have installed Procbot on your computer, you will need to get a bot token by creating an app `here <https://discordapp.com/developers/applications>`_.
You will then need to rename ``settings_example.json`` to ``settings.json`` and replace ``BOT_TOKEN_HERE`` with your bot token.

The following files must also be created:

.. code::

    guilds.json
    mod_logs.json
    xp.json

Each of these files must contain an empty dictionary:

.. code::

    {}

After you have configured the bot, open a command prompt or PowerShell window and do the following:

.. code:: sh

    drive>cd bot_directory
    bot_directory>python main.py

This will log the bot in to Discord, setting up the commands for use.

Requirements
------------

* Python 3.6.x (voice breaks with 3.7)
* ``discord`` library (`GitHub repository <https://github.com/Rapptz/discord.py/tree/rewrite>`_; **rewrite** branch required)
* ``youtube_dl`` library (`GitHub repository <https://github.com/rg3/youtube-dl>`_)
* Bot token from Discord
