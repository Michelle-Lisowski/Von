# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import json
from main import Von


def get_token():
    with open("config.json") as f:
        config = json.load(f)

    token = config["token"]
    return token


def main():
    token = get_token()
    bot = Von()
    bot.run(token)


if __name__ == "__main__":
    main()
