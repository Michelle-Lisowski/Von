# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess
import sys

try:
    from json.decoder import JSONDecodeError
    from main import Von
except ImportError:
    pass


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--upgrade", help="upgrade dependencies", action="store_true")
args = parser.parse_args()


def token_input():
    return input(">>> ")


def load_config():
    print("Loading config.json...")
    try:
        f = open("config.json")
    except FileNotFoundError:
        print("Creating config.json...", end="\r")
        open("config.json", "w")
        print("Creating config.json... done")
        f = open("config.json")

    print("Loading config.json dictionary...")
    try:
        json.load(f)
    except JSONDecodeError:
        print("Creating config.json dictionary...", end="\r")
        with open("config.json", "w") as f:
            f.write("{}")
            print("Creating config.json dictionary... done")

    with open("config.json") as f:
        config = json.load(f)

    print("Loaded config.json")
    return config


def check_db():
    print("Loading prefixes.json...")
    try:
        f = open("prefixes.json")
    except FileNotFoundError:
        print("Creating prefixes.json...", end="\r")
        open("prefixes.json", "w")
        print("Creating prefixes.json... done")
        f = open("prefixes.json")

    print("Loading prefixes.json dictionary...")
    try:
        json.load(f)
    except JSONDecodeError:
        print("Creating prefixes.json dictionary...", end="\r")
        with open("prefixes.json", "w") as f:
            f.write("{}")
            print("Creating prefixes.json dictionary... done")
    print("Loaded prefixes.json")


def install_dependencies():
    arguments = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    if args.upgrade:
        arguments.insert(4, "--upgrade")
    subprocess.call(arguments)


def main():
    print("Checking Python version...")

    if not sys.version_info >= (3, 6, 2):
        print("Python 3.6.2 or above is required. Please update Python and try again.")
        sys.exit(1)

    config = load_config()
    try:
        token = config["token"]
    except KeyError:
        print("Token not set. Please enter a token below.")
        token = token_input()

        with open("config.json", "w") as f:
            print("Writing token to config.json...", end="\r")
            config["token"] = token

            json.dump(config, f, indent=4)
            print("Writing token to config.json... done")

    print("Checking existence of database files...")
    check_db()

    print("Installing dependencies...")
    try:
        install_dependencies()
    except:
        print("Dependency installation failed.")
        sys.exit(1)

    print("Setup complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
