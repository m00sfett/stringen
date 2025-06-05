# stringen (v0.4.0)

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

- Calculate the length and entropies for an arbitrary string via `-r STRING`
- Configurable string length via positional `NUMBER`
- Optional Binary output (`-b`/`-2`/`--bin`)
- Optional Octal output (`-o`/`-8`/`--oct`)
- Optional digits (`-i`, `-10`, `--dec`)
- Optional lowercase letters (`-a`)
- Optional uppercase letters (`-A`)
- Optional Hexadecimal output (`-x`/`-16`/`--hex`) respecting `-a`/`-A` for case
- Hexadecimal mode uses random case when `-a` and `-A` are both omitted or both present
- Optional special characters (`-s [STRING|CHARSET_FILE]`, defaults to `charsets/special_charset_default.txt`)
- Read input from or write output to a file via `-f [FILE]`
- Aborts when the provided string contains non-printable characters
- Displays length, Shannon and password entropy
- Displays the recognized numeric base of the output
- Clean output with `-c` for scripting
- Help available via `-h`/`--help`
- Version information via `-V`/`--version`

## Usage

Below are a few common invocation examples:

```shell
# Show help and available options
python -m stringen --help

# Generate a 16 character password using letters and digits
python -m stringen -a -A -i 16
# > G9kLm8bTzYqH3W7P

# Generate a password with only lowercase letters and digits
python -m stringen -aAi 8
# > a3h9d2kj
 
# Binary and octal output
python -m stringen -b 16
# > 0101011010101010
python -m stringen -o 12
# > 735412607214

# Display the entropy of an existing string
python -m stringen -r hr5A8nPf5
# > Length: 9
# > Shannon entropy: 4.85 bits/char (43.63 bits total)
# > Password entropy: 58.49 bits

# Create a hexadecimal string
python -m stringen -x 32
# > 2A1F3B5E7D8C9A1F3E2B7C4D9F0E6A5C

# Include custom special characters
python -m stringen -s '!@#' 10
# > @!@!#!!@#!

# Print only the password entropy value
python -m stringen -c -r hr5A8nPf5
# > 58.49

# Write the generated string to a file
python -m stringen -f output.txt 12
# > (writes e.g. W8YzKp3N2dFq to output.txt)

# Read lines from a file to calculate their entropies
python -m stringen -r -f input.txt
# > read from file input.txt:
# > string: password123
# > Length: 11
# > Shannon entropy: 3.18 bits/char (34.94 bits total)
# > Password entropy: 65.79 bits
# > string: qwerty!
# > Length: 7
# > Shannon entropy: 2.80 bits/char (19.60 bits total)
# > Password entropy: 42.09 bits
```

## Entropy

The tool reports Shannon entropy and password entropy for both generated and
provided strings. *Shannon entropy* measures the average information contained
in the string, while *password entropy* estimates how strong a password is based
on its length and character set size. Both values are given in bits&mdash;higher
numbers indicate a harder to guess string.

For secure password generation, choose a sufficiently long length.
Short strings offer little entropy and are easier to guess.
