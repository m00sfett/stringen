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

# Generate a password with only lowercase letters and digits
python -m stringen -aAi 8

# Binary and octal output
python -m stringen -b 16
python -m stringen -o 12

# Display the entropy of an existing string
python -m stringen -r hr5A8nPf5

# Create a hexadecimal string
python -m stringen -x 32

# Include custom special characters
python -m stringen -s '!@#' 10

# Print only the entropy value
python -m stringen -c -r hr5A8nPf5

# Write the generated string to a file
python -m stringen -f output.txt 12

# Read lines from a file to calculate their entropies
python -m stringen -r ignored -f input.txt
```

## Entropy

The tool reports Shannon entropy and password entropy for both generated and
provided strings. *Shannon entropy* measures the average information contained
in the string, while *password entropy* estimates how strong a password is based
on its length and character set size. Both values are given in bits&mdash;higher
numbers indicate a harder to guess string.

For secure password generation, choose a sufficiently long length.
Short strings offer little entropy and are easier to guess.
