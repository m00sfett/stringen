# stringen (v0.0.2)

A simple command line string generator written in Python. If no character set
is selected, lowercase letters, uppercase letters and digits are used by
default. The generated string length defaults to 12 characters.

## Features
- Optional lowercase letters (`-a`)
- Optional uppercase letters (`-A`)
- Optional digits (`-i`)
- Hexadecimal output (`-h`) respecting `-a`/`-A` for case
- Configurable string length via `-c <NUMBER>`
- Displays Shannon entropy of the generated string

## Usage
```
python -m stringen -a -A -i -c 16
```
