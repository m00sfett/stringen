"""Utility functions for string generation and entropy calculations."""

from __future__ import annotations

import argparse
import math
import secrets
import string
from collections import Counter


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

    if not (args.lower or args.upper or args.digits):
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


def password_entropy(text: str) -> float:
    """Return password entropy based on character set size and length."""
    if not text:
        return 0.0
    hex_chars = set("0123456789abcdefABCDEF")
    text_set = set(text)
    if text_set <= hex_chars and any(c.isalpha() for c in text):
        charset = 16
    elif text_set <= {"0", "1"}:
        charset = 2
    elif text_set <= set("01234567"):
        charset = 8
    elif text_set <= set(string.digits):
        charset = 10
    else:
        charset = 0
        if any(c.islower() for c in text):
            charset += 26
        if any(c.isupper() for c in text):
            charset += 26
        if any(c.isdigit() for c in text):
            charset += 10
    if charset == 0:
        return 0.0
    return len(text) * math.log2(charset)

