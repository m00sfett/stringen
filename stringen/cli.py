"""Command line interface for the stringen package."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .utils import (
    build_charset,
    generate_string,
    password_entropy,
    positive_int,
    shannon_entropy,
)


class HelpOnErrorParser(argparse.ArgumentParser):
    """Argument parser that shows help on error."""

    def error(self, message: str) -> None:
        self.print_help(sys.stderr)
        self.exit(2, f"{self.prog}: error: {message}\n")


def parse_args(
    arguments: list[str] | None = None,
) -> tuple[argparse.Namespace, argparse.ArgumentParser]:
    """Return parsed command line arguments and the parser."""
    parser = HelpOnErrorParser(
        description="Simple string generator",
        add_help=False,
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="show this help message and exit",
    )
    parser.add_argument(
        "-a",
        "--lower",
        action="store_true",
        help="include lowercase letters (a-z)",
    )
    parser.add_argument(
        "-A",
        "--upper",
        action="store_true",
        help="include uppercase letters (A-Z)",
    )
    parser.add_argument(
        "-i",
        "--digits",
        action="store_true",
        help="include digits (0-9)",
    )
    parser.add_argument(
        "-x",
        "--hex",
        action="store_true",
        help="output hexadecimal string (uses -a/-A for case)",
    )
    parser.add_argument(
        "-r",
        "--entropy",
        metavar="STRING",
        help="calculate entropies for STRING and exit",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="display only the generated password or entropy",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"stringen {__version__}",
        help="show program's version number and exit",
    )
    parser.add_argument(
        "length",
        type=positive_int,
        nargs="?",
        default=12,
        help="length of the generated string",
    )
    return parser.parse_args(arguments), parser


def main() -> None:
    """Entry point for the command line interface."""
    args, parser = parse_args()
    if args.entropy is not None:
        text_length = len(args.entropy)
        sh_entropy = shannon_entropy(args.entropy)
        pw_entropy = password_entropy(args.entropy)
        if args.clean:
            print(f"{pw_entropy:.2f}")
            return
        print(f"Length: {text_length}")
        print(f"Shannon entropy: {sh_entropy:.2f} bits")
        print(f"Password entropy: {pw_entropy:.2f} bits")
        return

    charset = build_charset(args)
    if not charset:
        parser.error("No character set selected. Use -a, -A, -i or -x")

    result = generate_string(args.length, charset)
    if args.clean:
        print(result)
        return
    result_length = len(result)
    sh_entropy = shannon_entropy(result)
    pw_entropy = password_entropy(result)
    print(result)
    print(f"Length: {result_length}")
    print(f"Shannon entropy: {sh_entropy:.2f} bits")
    print(f"Password entropy: {pw_entropy:.2f} bits")

