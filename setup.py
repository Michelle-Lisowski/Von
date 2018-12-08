# -*- coding: utf-8 -*-

from bot import Von
from utils import set_token


def exit(code):
    try:
        raise SystemExit(code)
    except SystemExit:
        return


def main():
    print("Checking for token...")
    set_token()

    print("Setup complete.")
    exit(0)


if __name__ == "__main__":
    main()
