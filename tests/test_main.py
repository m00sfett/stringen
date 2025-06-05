import string
import sys
import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]

cli_spec = importlib.util.spec_from_file_location(
    'stringen.cli',
    ROOT / 'stringen' / 'cli.py',
)
cli = importlib.util.module_from_spec(cli_spec)
cli_spec.loader.exec_module(cli)

utils_spec = importlib.util.spec_from_file_location(
    'stringen.utils',
    ROOT / 'stringen' / 'utils.py',
)
utils = importlib.util.module_from_spec(utils_spec)
utils_spec.loader.exec_module(utils)

parse_args = cli.parse_args
main = cli.main
build_charset = utils.build_charset
password_entropy = utils.password_entropy


def test_length_validation():
    with pytest.raises(SystemExit):
        parse_args(['0'])


def test_default_charset():
    args, _ = parse_args([])
    charset = build_charset(args)
    expected = string.ascii_lowercase + string.ascii_uppercase + string.digits
    assert set(charset) == set(expected)


def test_hex_random_case_no_flags():
    args, _ = parse_args(['-x'])
    charset = build_charset(args)
    assert charset == string.digits + 'abcdefABCDEF'


def test_hex_random_case_both_flags():
    args, _ = parse_args(['-x', '-a', '-A'])
    charset = build_charset(args)
    assert charset == string.digits + 'abcdefABCDEF'


def test_hex_lowercase_only():
    args, _ = parse_args(['-x', '-a'])
    charset = build_charset(args)
    assert charset == string.digits + 'abcdef'


def test_hex_uppercase_only():
    args, _ = parse_args(['-x', '-A'])
    charset = build_charset(args)
    assert charset == string.digits + 'ABCDEF'


def test_clean_flag_parsing():
    args, _ = parse_args(['-c'])
    assert args.clean is True


def test_main_clean_generation(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['stringen', '-c', '5'])
    main()
    captured = capsys.readouterr()
    output = captured.out.strip().splitlines()
    assert len(output) == 1
    assert len(output[0]) == 5


def test_main_clean_entropy(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['stringen', '-c', '-r', 'abc'])
    main()
    captured = capsys.readouterr()
    expected = f"{password_entropy('abc'):.2f}"
    assert captured.out.strip() == expected
