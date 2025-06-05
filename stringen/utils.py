"""Utility functions for string generation and entropy calculations."""

from __future__ import annotations

import argparse
import math
import secrets
import string
from collections import Counter
from pathlib import Path


def positive_int(value: str) -> int:
    """Return a positive integer or raise ``ArgumentTypeError``."""
    try:
        ivalue = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("length must be a positive integer")
    return ivalue


def build_charset(args: argparse.Namespace) -> str:
    """Return a character set string based on provided flags."""
    if args.hex:
        if args.lower and not args.upper:
            return string.digits + "abcdef"
        if args.upper and not args.lower:
            return string.digits + "ABCDEF"
        return string.digits + "abcdefABCDEF"
    if args.bin:
        return "01"
    if args.oct:
        return "01234567"

    if not (args.lower or args.upper or args.digits or args.spec is not None):
        use_lower = use_upper = use_digits = True
    else:
        use_lower = args.lower
        use_upper = args.upper
        use_digits = args.digits

    charset = ""
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    if args.spec is not None:
        if args.spec == "":
            path = Path(__file__).resolve().parent / "charsets" / "special_charset_default.txt"
        else:
            p = Path(args.spec)
            path = p if p.is_file() else None
        try:
            if path is None:
                spec_chars = args.spec
            else:
                spec_chars = path.read_text(encoding="utf-8").strip()
        except OSError as exc:
            raise argparse.ArgumentTypeError(str(exc))
        charset += spec_chars
    return charset


def generate_string(length: int, charset: str) -> str:
    """Generate string of given length from charset using secrets."""
    return "".join(secrets.choice(charset) for _ in range(length))


def shannon_entropy(text: str) -> float:
    """Return Shannon entropy of the given text."""
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    return -sum(
        (count / length) * math.log2(count / length)
        for count in freq.values()
    )


def recognized_base(text: str) -> int:
    """Return recognized numeric base of the given text."""
    if not text:
        return 0
    hex_chars = set("0123456789abcdefABCDEF")
    text_set = set(text)
    if text_set <= hex_chars and any(c.isalpha() for c in text):
        return 16
    if text_set <= {"0", "1"}:
        return 2
    if text_set <= set("01234567"):
        return 8
    if text_set <= set(string.digits):
        return 10
    return 0


def password_entropy(text: str) -> float:
    """Return password entropy based on character set size and length."""
    if not text:
        return 0.0
    charset = recognized_base(text)
    if charset == 0:
        if any(c.islower() for c in text):
            charset += 26
        if any(c.isupper() for c in text):
            charset += 26
        if any(c.isdigit() for c in text):
            charset += 10
    if charset == 0:
        return 0.0
    return len(text) * math.log2(charset)

