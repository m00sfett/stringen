"""Tests for the stringen command line interface and utilities."""

import string
import sys
import pytest

from stringen.cli import parse_args, main
from stringen.utils import build_charset, password_entropy


def test_length_validation():
    """parse_args exits when an invalid length is provided."""
    with pytest.raises(SystemExit):
        parse_args(['0'])


def test_default_charset():
    """build_charset returns the default set when no flags are given."""
    args, _ = parse_args([])
    charset = build_charset(args)
    expected = string.ascii_lowercase + string.ascii_uppercase + string.digits
    assert set(charset) == set(expected)


def test_hex_random_case_no_flags():
    """Hex output uses mixed case when neither -a nor -A is provided."""
    args, _ = parse_args(['-x'])
    charset = build_charset(args)
    assert charset == string.digits + 'abcdefABCDEF'


def test_hex_random_case_both_flags():
    """Hex output also uses mixed case when -a and -A are combined."""
    args, _ = parse_args(['-x', '-a', '-A'])
    charset = build_charset(args)
    assert charset == string.digits + 'abcdefABCDEF'


def test_hex_lowercase_only():
    """Hex output respects -a for lowercase only."""
    args, _ = parse_args(['-x', '-a'])
    charset = build_charset(args)
    assert charset == string.digits + 'abcdef'


def test_hex_uppercase_only():
    """Hex output respects -A for uppercase only."""
    args, _ = parse_args(['-x', '-A'])
    charset = build_charset(args)
    assert charset == string.digits + 'ABCDEF'


def test_digits_aliases():
    """The -10/--dec flags map to digits."""
    args1, _ = parse_args(['-10'])
    args2, _ = parse_args(['--dec'])
    assert args1.digits and args2.digits


def test_hex_alias():
    """The -16 flag maps to hexadecimal output."""
    args, _ = parse_args(['-16'])
    assert args.hex is True


def test_binary_charset():
    """Binary mode uses only 0 and 1."""
    args, _ = parse_args(['-b'])
    charset = build_charset(args)
    assert charset == '01'


def test_octal_charset():
    """Octal mode uses digits 0-7."""
    args, _ = parse_args(['-o'])
    charset = build_charset(args)
    assert charset == '01234567'


def test_clean_flag_parsing():
    """The -c flag is parsed correctly."""
    args, _ = parse_args(['-c'])
    assert args.clean is True


def test_main_clean_generation(monkeypatch, capsys):
    """Main outputs only the generated string when -c is used."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-c', '5'])
    main()
    captured = capsys.readouterr()
    output = captured.out.strip().splitlines()
    assert len(output) == 1
    assert len(output[0]) == 5


def test_main_clean_entropy(monkeypatch, capsys):
    """Main prints only the password entropy in clean mode."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-c', '-r', 'abc'])
    main()
    captured = capsys.readouterr()
    expected = f"{password_entropy('abc'):.2f}"
    assert captured.out.strip() == expected
