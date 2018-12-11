# -*- coding: utf-8 -*-

import sys

try:
    from bot import Von
except SyntaxError:
    pass


def main():
    if not sys.version_info >= (3, 6):
        print("Python 3.6 or above is required to run Von.")
        sys.exit(1)
    Von().run()


if __name__ == "__main__":
    main()
