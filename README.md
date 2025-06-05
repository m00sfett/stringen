# stringen (v0.0.3)

A simple command line string generator written in Python. If no character set
is selected, lowercase letters, uppercase letters and digits are used by
default. The generated string length defaults to 12 characters.

## Features
- Optional lowercase letters (`-a`)
- Optional uppercase letters (`-A`)
- Optional digits (`-i`)
- Hexadecimal output (`-h`) respecting `-a`/`-A` for case
- Configurable string length via positional `NUMBER`
- Displays Shannon entropy of the generated string
- Calculate Shannon and password entropy for an arbitrary string via `-r STRING`

## Usage
```
python -m stringen -a -A -i 16
python -m stringen -r hr5A8nPf5
```
