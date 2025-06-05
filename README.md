# stringen (v0.3.1)

A simple command line string generator written in Python. If no character set
is selected, lowercase letters, uppercase letters and digits are used by
default. The generated string length defaults to 12 characters.

## Running

No installation is required. Execute the tool directly from the project
directory:

```shell
python -m stringen --help
```

## Features

- Optional lowercase letters (`-a`)
- Optional uppercase letters (`-A`)
- Optional digits (`-i`, `-10`, `--dec`)
- Binary output (`-b`/`-2`/`--bin`)
- Octal output (`-o`/`-8`/`--oct`)
- Hexadecimal output (`-x`/`-16`/`--hex`) respecting `-a`/`-A` for case
- Help available via `-h`/`--help`
- Version information via `-V`/`--version`
- Configurable string length via positional `NUMBER`
- Displays length, Shannon and password entropy of the generated string
- Calculate the length and entropies for an arbitrary string via `-r STRING`
- Clean output with `-c` for scripting
- Hexadecimal mode uses random case when `-a` and `-A` are both omitted or both
  present
- Displays the recognized numeric base of the output
- The `NUMBER` argument must be a positive integer

## Usage

```shell
python -m stringen --help
python -m stringen -a -A -i 16
python -m stringen -aAi 8
python -m stringen -b 16
python -m stringen -o 12
python -m stringen -r hr5A8nPf5
python -m stringen -x 32
python -m stringen -c -r hr5A8nPf5
```

## Entropy

The tool reports Shannon entropy and password entropy for both generated and
provided strings. *Shannon entropy* measures the average information contained
in the string, while *password entropy* estimates how strong a password is based
on its length and character set size. Both values are given in bits&mdash;higher
numbers indicate a harder to guess string.

For secure password generation, choose a sufficiently long length.
Short strings offer little entropy and are easier to guess.
