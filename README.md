# stringen (v0.0.4)

A simple command line string generator written in Python. If no character set
is selected, lowercase letters, uppercase letters and digits are used by
default. The generated string length defaults to 12 characters.

## Features

- Optional lowercase letters (`-a`)
- Optional uppercase letters (`-A`)
- Optional digits (`-i`)
- Hexadecimal output (`-h`) respecting `-a`/`-A` for case
- Configurable string length via positional `NUMBER`
- Displays Shannon and password entropy of the generated string
- Calculate the entropies for an arbitrary string via `-r STRING`

## Usage

```shell
python -m stringen -a -A -i 16
python -m stringen -r hr5A8nPf5
```
