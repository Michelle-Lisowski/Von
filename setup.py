# -*- coding: utf-8 -*-

import argparse
import sys

try:
    from bot import Von
except (ImportError, SyntaxError):
    pass


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--run", help="run bot", action="store_true")
args = parser.parse_args()


def main():
    if not sys.version_info >= (3, 6):
        print("Python 3.6 or above is required to run Von.")
        sys.exit(1)

    print("Setup complete.")
    if args.run:
        Von().run()
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
