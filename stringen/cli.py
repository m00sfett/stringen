"""Command line interface for the stringen package."""

from __future__ import annotations

import argparse
import logging
import sys

from . import __version__
from .utils import (
    build_charset,
    generate_string,
    generate_string_mixed,
    recognized_base,
    password_entropy,
    positive_int,
    shannon_entropy,
)

logger = logging.getLogger(__name__)


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
        "-10",
        "--dec",
        dest="digits",
        action="store_true",
        help="include digits (0-9)",
    )
    parser.add_argument(
        "-x",
        "--hex",
        "-16",
        dest="hex",
        action="store_true",
        help="output hexadecimal string (uses -a/-A for case)",
    )
    parser.add_argument(
        "-b",
        "-2",
        "--bin",
        dest="bin",
        action="store_true",
        help="output binary string",
    )
    parser.add_argument(
        "-o",
        "-8",
        "--oct",
        dest="oct",
        action="store_true",
        help="output octal string",
    )
    parser.add_argument(
        "-s",
        "--spec",
        nargs="?",
        const="",
        metavar="STRING|FILE",
        help=(
            "include special characters from STRING or FILE "
            "(default: charsets/special_charset_default.txt)"
        ),
    )
    parser.add_argument(
        "-r",
        "--entropy",
        nargs="?",
        const="",
        metavar="STRING",
        help="calculate entropies for STRING or each line in FILE",
    )
    parser.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="display only the generated password or entropy",
    )
    parser.add_argument(
        "-f",
        "--file",
        nargs="?",
        const=".",
        metavar="FILE",
        help="read input from or write output to FILE (default: .)",
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
    if arguments is None:
        arguments = sys.argv[1:]
    processed: list[str] = []
    for arg in arguments:
        if arg == "-rf":
            # Allow the short option combination "-rf" to behave like
            # passing "-r" and "-f" separately.
            processed.extend(["-r", "-f"])
        else:
            processed.append(arg)
    return parser.parse_args(processed), parser


def main() -> None:
    """Entry point for the command line interface."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.handlers = [handler]
    logger.setLevel(logging.INFO)
    args, parser = parse_args()
    if args.entropy is not None and args.file is None:
        if args.entropy == "":
            parser.error("missing string")
        if any(ord(ch) < 32 or ord(ch) > 126 for ch in args.entropy):
            parser.error("illegal characters")
        text_length = len(args.entropy)
        sh_entropy = shannon_entropy(args.entropy)
        sh_total = sh_entropy * text_length
        pw_entropy = password_entropy(args.entropy)
        base = recognized_base(args.entropy)
        if args.clean:
            logger.info(f"{pw_entropy:.2f}")
            return
        logger.info(f"Length: {text_length}")
        logger.info(
            f"Shannon entropy: {sh_entropy:.2f} bits/char ({sh_total:.2f} bits total)"
        )
        logger.info(f"Password entropy: {pw_entropy:.2f} bits")
        logger.info(f"Base: {base}")
        return

    if args.file is not None and args.entropy is not None:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                lines = [line.rstrip("\n") for line in fh]
                lines = [ln for ln in lines if ln]
        except OSError as exc:
            parser.error(str(exc))
        logger.info(f"read from file {args.file}:")
        for idx, line in enumerate(lines, start=1):
            if line == "":
                continue
            if any(ord(ch) < 32 or ord(ch) > 126 for ch in line):
                parser.error("illegal characters")
            text_length = len(line)
            sh_entropy = shannon_entropy(line)
            sh_total = sh_entropy * text_length
            pw_entropy = password_entropy(line)
            base = recognized_base(line)
            label = f"Line: {idx}" if args.clean else f"string: {line}"
            logger.info(label)
            logger.info(f"Length: {text_length}")
            logger.info(
                f"Shannon entropy: {sh_entropy:.2f} bits/char ({sh_total:.2f} bits total)"
            )
            logger.info(f"Password entropy: {pw_entropy:.2f} bits")
            logger.info(f"Recognized base: {base}")
        return

    try:
        groups = build_charset(args, as_groups=True)
    except argparse.ArgumentTypeError as exc:
        parser.error(str(exc))
    charset = "".join(groups)
    if not charset:
        parser.error(
            "No character set selected. Use -a, -A, -i/-10, -b, -o or -x"
        )

    if len(groups) > 1:
        result = generate_string_mixed(args.length, groups)
    else:
        result = generate_string(args.length, charset)
    if args.file is not None:
        try:
            with open(args.file, "w", encoding="utf-8") as fh:
                fh.write(result)
        except OSError as exc:
            parser.error(str(exc))
        if args.clean:
            return
        result_length = len(result)
        sh_entropy = shannon_entropy(result)
        sh_total = sh_entropy * result_length
        pw_entropy = password_entropy(result)
        base = recognized_base(result)
        logger.info(f"Length: {result_length}")
        logger.info(
            f"Shannon entropy: {sh_entropy:.2f} bits/char ({sh_total:.2f} bits total)"
        )
        logger.info(f"Password entropy: {pw_entropy:.2f} bits")
        logger.info(f"Recognized base: {base}")
        return
    if args.clean:
        logger.info(result)
        return
    result_length = len(result)
    sh_entropy = shannon_entropy(result)
    sh_total = sh_entropy * result_length
    pw_entropy = password_entropy(result)
    base = recognized_base(result)
    logger.info(result)
    logger.info(f"Length: {result_length}")
    logger.info(
        f"Shannon entropy: {sh_entropy:.2f} bits/char ({sh_total:.2f} bits total)"
    )
    logger.info(f"Password entropy: {pw_entropy:.2f} bits")
    logger.info(f"Recognized base: {base}")

