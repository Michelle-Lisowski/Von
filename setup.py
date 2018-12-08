# -*- coding: utf-8 -*-

import argparse

from bot import Von

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--run", help="run bot", action="store_true")
args = parser.parse_args()


def exit(code):
    try:
        raise SystemExit(code)
    except SystemExit:
        return


def main():
    print("Setup complete.")
    if args.run:
        Von().run()
    else:
        exit(0)


if __name__ == "__main__":
    main()
