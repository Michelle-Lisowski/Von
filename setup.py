# Von V2
# Copyright (c) 2018 sirtezza451
# -*- coding: utf-8 -*-

import argparse
import json
import subprocess
import sys
from json.decoder import JSONDecodeError
from subprocess import CalledProcessError
from os.path import isdir

from main import Von

print("Checking Python version...")

if not sys.version_info >= (3, 6, 2):
    print("Python 3.6.2 or above is required. Please update Python and try again.")
    sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-u", "--upgrade-deps", help="upgrade dependencies", action="store_true"
)
parser.add_argument(
    "-p", "--update-bot", help="pull code from git repository", action="store_true"
)
args = parser.parse_args()


def token_input():
    return input(">>> ")


def is_venv():
    return hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )


# def yes_no_input(msg):
    # print(f"{msg} [y/n]")
    # i = input(">>>")

    # if i.lower() in ["yes", "y"]


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
    files = ["experience.json", "prefixes.json", "settings.json"]

    for file in files:
        print(f"Loading {file}...")
        try:
            f = open(file)
        except FileNotFoundError:
            print(f"Creating {file}...", end="\r")
            open(file, "w")
            print(f"Creating {file}... done")
            f = open(file)

        print(f"Loading {file} dictionary...")
        try:
            json.load(f)
        except JSONDecodeError:
            print(f"Creating {file} dictionary...", end="\r")
            with open(file, "w") as f:
                f.write("{}")
                print(f"Creating {file} dictionary... done")
        print(f"Loaded {file}")


def install_dependencies():
    arguments = [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    if args.upgrade_deps:
        arguments.insert(4, "--upgrade")
    if not is_venv():
        arguments.insert(4, "--user")
    command = " ".join(arguments)

    try:
        subprocess.check_call(command, shell=True)
    except CalledProcessError:
        print("Dependency installation failed.")
        sys.exit(1)


def update_bot():
    print("Checking for Git Bash...")
    if not isdir(".git"):
        print(
            "You have not cloned Von from the repository using Git.",
            "This means it is not possible to update Von from the command line.",
            sep="\n",
        )
        sys.exit(1)

    try:
        subprocess.check_call("git --version", shell=True)
    except CalledProcessError:
        print(
            "Make sure Git Bash is installed on your system.",
            "If it is, make sure you have set it up to run from the command line.",
            sep="\n",
        )
        sys.exit(1)

    print("Passed Git Bash checks...")

    print(
        "If you have made any modifications to the source code yourself, you will",
        "lose them by updating. Are you sure you want to update? [y/n]",
    )

    yn = input(">>> ")

    if yn.lower() in ["yes", "y"]:
        try:
            subprocess.check_call("git pull", shell=True)
        except CalledProcessError:
            print("Updating Von failed. Try running 'git pull' yourself.")
            sys.exit(1)
    else:
        print("Skipping update...")
        return


def main():
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
    install_dependencies()

    if args.update_bot:
        print("Updating bot...")
        update_bot()

    print("Setup complete.")
    sys.exit(0)


if __name__ == "__main__":
    main()
