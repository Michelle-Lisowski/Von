# -*- coding: utf-8 -*-

import sys

try:
    from bot import Von
except (ImportError, ModuleNotFoundError):
    print(
        "The bot class could not be imported, which means",
        "that it is not able to be run. Make sure you don't",
        "have any missing files. If you do, you'll need to",
        "either clone the GitHub repository, update the code",
        "using the 'git pull' command. This will only work",
        "inside the folder of a cloned GitHub repositry.",
    )
    sys.exit(1)
except SyntaxError:
    pass


def main():
    if not sys.version_info >= (3, 6):
        print("Python 3.6 or above is required to run Von.")
        sys.exit(1)
    Von().run()


if __name__ == "__main__":
    __name__ = "launcher"
    main()
