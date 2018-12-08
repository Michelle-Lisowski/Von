# -*- coding: utf-8 -*-

import json
from json.decoder import JSONDecodeError


def set_token():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        with open("config.json", "w") as f:
            f.write("{}")

        with open("config.json") as f:
            config = json.load(f)

    try:
        token = config["TOKEN"]
    except KeyError:
        print("Enter your token from Discord below.")
        config["TOKEN"] = input(">>> ")
        token = config["TOKEN"]

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
    return token
