# stringen (v0.1.0)

A simple command line string generator written in Python. If no character set
is selected, lowercase letters, uppercase letters and digits are used by
default. The generated string length defaults to 12 characters.

## Features

- Optional lowercase letters (`-a`)
- Optional uppercase letters (`-A`)
- Optional digits (`-i`)
- Hexadecimal output (`-x`) respecting `-a`/`-A` for case
- Help available via `-h`/`--help`
- Configurable string length via positional `NUMBER`
- Displays length, Shannon and password entropy of the generated string
- Calculate the length and entropies for an arbitrary string via `-r STRING`

## Usage

```shell
python -m stringen --help
python -m stringen -a -A -i 16
python -m stringen -aAi 8
python -m stringen -r hr5A8nPf5
python -m stringen -x 32
```
