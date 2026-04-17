from __future__ import annotations

import sys

from monarch_api import MonarchHTTPError

from .parser import build_parser
from .style import print_help_all


def main() -> None:
    argv = sys.argv[1:]
    parser, parsers = build_parser()

    if len(argv) >= 2 and argv[-2] in {"-h", "--help"} and argv[-1] == "all":
        print_help_all(parsers)
        return

    args = parser.parse_args(argv)

    try:
        args.func(args)
    except MonarchHTTPError as exc:
        raise SystemExit(str(exc)) from exc
