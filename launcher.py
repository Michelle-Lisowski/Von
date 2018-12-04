# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json
import logging
import sys

from aiohttp.client_exceptions import ClientConnectorError

from main import Von


def get_token():
    with open("config.json") as f:
        config = json.load(f)

    token = config["token"]
    return token


def setup_logging():
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)

    handler = logging.FileHandler("discord.log", encoding="utf-8", mode="w")
    handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] %(name)s: %(message)s")
    )

    logger.addHandler(handler)
    return logger


def main():
    print("Setting up logging...", end="\r")
    setup_logging()

    print("Setting up logging... done")
    token = get_token()

    try:
        Von().run(token)
    except ClientConnectorError:
        print(
            "An error occurred while logging in.",
            "Make sure you have an internet connection and try again.",
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
