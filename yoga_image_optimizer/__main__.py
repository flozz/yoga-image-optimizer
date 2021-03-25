import sys
import argparse

from .application import YogaImageOptimizerApplication
from . import VERSION


def main(args=sys.argv):
    # Basic CLI using argparse (simpler than using GTK Application CLI)
    cli_parser = argparse.ArgumentParser()
    cli_parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=VERSION,
    )
    cli_parser.add_argument(
        "image",
        nargs="*",
        help="Input image",
    )
    cli_parser.parse_args(args[1:])

    # GTK Application
    app = YogaImageOptimizerApplication()
    app.run(args)


if __name__ == "__main__":
    main()
