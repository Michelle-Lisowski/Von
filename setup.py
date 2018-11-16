# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess
import sys

try:
    from json import JSONDecodeError
    from main import Von
except ImportError:
    pass


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--upgrade", help="upgrade dependencies", action="store_true")
args = parser.parse_args()


def token_input():
    return input(">>> ")


def read_config():
    return open("config.json")


def write_config():
    return open("config.json", "w")


def read_prefixes():
    return open("prefixes.json")


def write_prefixes():
    return open("prefixes.json", "w")


def check_config():
    try:
        print("Reading config.json...")
        read_config()
    except FileNotFoundError:
        print("config.json doesn't exist;")
        print("Creating config.json...", end="\r")

        write_config()
        print("Creating config.json... done")

    with read_config() as f:
        try:
            print("Loading config.json dictionary...")
            config = json.load(f)
        except JSONDecodeError:
            print("config.json doesn't contain a dictionary, creating...")

            with write_config() as f:
                print("Writing to config.json...", end="\r")
                f.write("{}")

                print("Writing to config.json... done")

            with read_config() as f:
                config = json.load(f)

        print("config.json loaded")
        return config


def check_prefixes():
    try:
        print("Reading prefixes.json...")
        read_prefixes()
    except FileNotFoundError:
        print("prefixes.json doesn't exist;")
        print("Creating prefixes.json...", end="\r")

        write_prefixes()
        print("Creating prefixes.json... done")

    with read_prefixes() as f:
        try:
            print("Loading prefixes.json dictionary...")
            json.load(f)
        except JSONDecodeError:
            print("prefixes.json doesn't contain a dictionary, creating...")

            with write_prefixes() as f:
                print("Writing to prefixes.json...", end="\r")
                f.write("{}")

                print("Writing to prefixes.json... done")
        print("prefixes.json loaded")
        

def install_dependencies():
    if args.upgrade:
        subprocess.call(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "-r",
                "requirements.txt",
            ]
        )
    else:
        subprocess.call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )


def main():
    print("Checking Python version...")

    if not sys.version_info >= (3, 6, 2):
        print("Python 3.6.2 or above is required. Please update Python and try again.")
        sys.exit(1)

    print("Checking configuration...")
    config = check_config()

    try:
        token = config["token"]
    except KeyError:
        print("Token doesn't exist. Please enter a token below.")
        token = token_input()

        with write_config() as f:
            print("Writing to config.json...")
            config["token"] = token
            json.dump(config, f, indent=4)

    print("Checking guild prefixes...")
    check_prefixes()

    try:
        print("Installing dependencies...")
        install_dependencies()
    except:
        print("Dependency installation failed.")

    print("Setup complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
