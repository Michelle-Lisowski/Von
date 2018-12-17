# -*- coding: utf-8 -*-

import json
from json.decoder import JSONDecodeError


def get_custom_settings():
    try:
        with open("custom.json") as f:
            custom = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        with open("custom.json", "w") as f:
            f.write("{}")

        with open("custom.json") as f:
            custom = json.load(f)
    return custom


def clean_region(region: str):
    """
    Returns a cleaned up string of a guild's
    voice region. For example, `vip-us-east`
    will become `VIP US East`.
    """
    split = region.split("-")
    strs = []

    if len(split) == 3:
        strs.append(split[0].upper())
        strs.append(split[1].upper())
        strs.append(split[2].capitalize())
    elif len(split) == 2:
        strs.append(split[0].upper())
        strs.append(split[1].capitalize())
    elif len(split) == 1:
        strs.append(split[0].capitalize())
    return " ".join(strs)


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
