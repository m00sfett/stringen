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


def build_charset(args: argparse.Namespace, *, as_groups: bool = False) -> str | list[str]:
    """Return a character set string or list of character groups."""
    if args.hex:
        charset = (
            string.digits + "abcdef"
            if args.lower and not args.upper
            else string.digits + "ABCDEF"
            if args.upper and not args.lower
            else string.digits + "abcdefABCDEF"
        )
        return [charset] if as_groups else charset
    if args.bin:
        return ["01"] if as_groups else "01"
    if args.oct:
        return ["01234567"] if as_groups else "01234567"

    if not (args.lower or args.upper or args.digits or args.spec is not None):
        use_lower = use_upper = use_digits = True
    else:
        use_lower = args.lower
        use_upper = args.upper
        use_digits = args.digits

    groups: list[str] = []
    if use_lower:
        groups.append(string.ascii_lowercase)
    if use_upper:
        groups.append(string.ascii_uppercase)
    if use_digits:
        groups.append(string.digits)
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
        groups.append(spec_chars)

    charset = "".join(groups)
    return groups if as_groups else charset


def generate_string(length: int, charset: str) -> str:
    """Generate string of given length from charset using secrets."""
    return "".join(secrets.choice(charset) for _ in range(length))


def generate_string_mixed(length: int, groups: list[str]) -> str:
    """Generate a string from multiple groups.

    When ``length`` is at least the number of groups, ensure the result contains
    one character from each group. Otherwise, select random characters from the
    combined set.
    """
    if not groups:
        return ""
    all_chars = "".join(groups)
    if length < len(groups):
        return generate_string(length, all_chars)
    result = [secrets.choice(group) for group in groups]
    for _ in range(length - len(groups)):
        result.append(secrets.choice(all_chars))
    secrets.SystemRandom().shuffle(result)
    return "".join(result)


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
    """Return recognized numeric base of the given text.

    The smallest base capable of representing all characters is returned.
    Hexadecimal is only detected when letters ``a``-``f`` or ``A``-``F`` are
    present.
    """
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


def character_set_size(text: str) -> int:
    """Return the size of the character set present in ``text``."""
    if not text:
        return 0
    base = recognized_base(text)
    if base:
        return base

    size = 0
    if any(c.islower() for c in text):
        size += 26
    if any(c.isupper() for c in text):
        size += 26
    if any(c.isdigit() for c in text):
        size += 10
    specials = {c for c in text if not c.isalnum()}
    size += len(specials)

    return size


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
        # Account for special characters by counting the unique symbols
        specials = {c for c in text if not c.isalnum()}
        charset += len(specials)
    if charset == 0:
        return 0.0
    return len(text) * math.log2(charset)

