"""Tests for the stringen command line interface and utilities."""

import string
import sys
from pathlib import Path
import math
import pytest

from stringen.cli import parse_args, main
from stringen.utils import build_charset, password_entropy, recognized_base


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


def test_spec_string_charset():
    """Special characters from a string are added to the charset."""
    args, _ = parse_args(['-s', '!@'])
    charset = build_charset(args)
    expected = '!@'
    assert charset == expected


def test_spec_file_charset(tmp_path):
    """Special characters can be loaded from a file."""
    p = tmp_path / 'spec.txt'
    p.write_text('!$')
    args, _ = parse_args(['-s', str(p)])
    charset = build_charset(args)
    expected = '!$'
    assert charset == expected


def test_spec_default_file():
    """Using -s without argument loads the default file."""
    args, _ = parse_args(['-s'])
    charset = build_charset(args)
    default_path = (
        Path(__file__).resolve().parent.parent
        / 'stringen'
        / 'charsets'
        / 'special_charset_default.txt'
    )
    default_chars = default_path.read_text().strip()
    assert charset == default_chars


def test_clean_flag_parsing():
    """The -c flag is parsed correctly."""
    args, _ = parse_args(['-c'])
    assert args.clean is True


def test_file_argument_default():
    """Using -f without a path defaults to the current directory."""
    args, _ = parse_args(['-f'])
    assert args.file == '.'


def test_file_argument_value():
    """The -f option accepts a custom file path."""
    args, _ = parse_args(['-f', 'foo.txt'])
    assert args.file == 'foo.txt'


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


def test_recognized_base():
    """recognized_base identifies standard numeric bases."""
    assert recognized_base('1010') == 2
    assert recognized_base('123') == 8
    assert recognized_base('7ab') == 16
    assert recognized_base('abc') == 16


def test_password_entropy_special_chars():
    """password_entropy counts unique special characters."""
    result = password_entropy('!@#$')
    assert result == pytest.approx(len('!@#$') * math.log2(4))


def test_main_base_output_entropy(monkeypatch, capsys):
    """Base information is the last line when using -r."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-r', '1010'])
    main()
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert lines[-1] == 'Base: 2 (Character Set: 2)'


def test_main_base_output_generation(monkeypatch, capsys):
    """Base information is the last line when generating a string."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-b', '4'])
    main()
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert lines[-1] == 'Recognized base: 2 (Character Set: 2)'


def test_main_entropy_from_file(monkeypatch, tmp_path, capsys):
    """Entropy is calculated for each line in the file."""
    p = tmp_path / 'input.txt'
    p.write_text('abc\n1010\n')
    monkeypatch.setattr(sys, 'argv', ['stringen', '-r', '-f', str(p)])
    main()
    captured = capsys.readouterr()
    lines = [l for l in captured.out.strip().splitlines() if l]
    assert 'Recognized base: 16 (Character Set: 16)' in lines
    assert 'Recognized base: 2 (Character Set: 2)' in lines


def test_main_entropy_from_file_clean(monkeypatch, tmp_path, capsys):
    """With -c, strings from the file are hidden but stats are shown."""
    p = tmp_path / 'input.txt'
    p.write_text('abc\n\n1010\n')
    monkeypatch.setattr(sys, 'argv', ['stringen', '-c', '-r', '-f', str(p)])
    main()
    captured = capsys.readouterr()
    lines = [l for l in captured.out.strip().splitlines() if l]
    assert lines[0].startswith('read from file')
    assert 'Line: 1' in lines
    assert 'Line: 2' in lines
    assert 'string:' not in captured.out


def test_main_generation_to_file(monkeypatch, tmp_path, capsys):
    """Generated strings are written to the file when -f is used."""
    out = tmp_path / 'out.txt'
    monkeypatch.setattr(sys, 'argv', ['stringen', '-f', str(out), '5'])
    main()
    text = out.read_text().strip()
    assert len(text) == 5
    captured = capsys.readouterr()
    lines = captured.out.strip().splitlines()
    assert 'Length:' in lines[0]


def test_main_mixed_special_chars(monkeypatch, capsys):
    """Generated strings include at least one special character when -s is used."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-c', '-a', '-A', '-i', '-s', '!@', '8'])
    main()
    generated = capsys.readouterr().out.strip()
    assert any(ch in '!@' for ch in generated)


def test_main_illegal_char_cli(monkeypatch):
    """Non printable characters in -r abort the program."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-r', 'abc\x01'])
    with pytest.raises(SystemExit):
        main()


def test_main_illegal_char_file(monkeypatch, tmp_path):
    """Non printable characters in input file abort the program."""
    p = tmp_path / 'bad.txt'
    p.write_text('abc\x01\n')
    monkeypatch.setattr(sys, 'argv', ['stringen', '-r', '-f', str(p)])
    with pytest.raises(SystemExit):
        main()


def test_main_length_shorter_than_groups(monkeypatch, capsys):
    """When length is less than the groups, output still has requested length."""
    monkeypatch.setattr(sys, 'argv', ['stringen', '-a', '-A', '-i', '2'])
    main()
    out = capsys.readouterr().out.strip()
    assert len(out.splitlines()[0]) == 2

