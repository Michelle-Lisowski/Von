# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import asyncio
import json
import sys

import discord
from discord.ext import commands

from main import Von


def user_input():
    return input(">>> ")

def get_token():
    try:
        with open("config.json") as f:
            try:
                config = json.load(f)
            except:
                print("Configuration file doesn't contain a dictionary. Exiting.")
                sys.exit(1)
    except FileNotFoundError:
        print("Configuration file doesn't exist. Exiting.")
        sys.exit(1)

    try:
        token = config["token"]
    except KeyError:
        print("Enter your Discord token below.")
        config["token"] = user_input()
        token = config["token"]

    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    return token

def main(token):
    loop = asyncio.get_event_loop()
    bot = Von()
    
    try:
        bot.run(token)
    except:
        print("Could not run Von. Exiting.")
        sys.exit(1)


if __name__ == "__main__":
    token = get_token()
    main(token)
