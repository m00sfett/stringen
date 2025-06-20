# Changelog

## 0.4.2

- Short option clusters ending with `-s` now load the default special
  characters when no argument is provided

## 0.4.1

- Skip empty lines when calculating entropy from files
- Hide secrets when using -c with -f by replacing the string with a line indicator
- Output label remains "Base" when calculating entropy directly

## 0.4.0

- Added `-s/--spec` option for custom special characters
- Included default and sample special character files

## 0.3.2

- Read and write strings via `-f [FILE]`
- Abort on illegal characters in provided strings

## 0.3.1

- Display recognized numeric base in output

## 0.3.0

- Added aliases `-10`/`--dec` for decimal digits
- Added aliases `-16` for hexadecimal output
- Added binary (`-b`/`-2`/`--bin`) and octal (`-o`/`-8`/`--oct`) modes
- Password entropy now recognizes binary, octal and decimal strings

## 0.2.1

- CLI output now uses the ``logging`` module
- Expanded README with an explanation of entropy values
- Tests import modules normally and include docstrings

## 0.2.0

- CLI moved to new ``stringen.cli`` module with typed functions
- Utility helpers moved to ``stringen.utils``
- Added ``-V/--version`` option
- Tests use ``importlib`` to load modules

## 0.1.2

- Added `-c/--clean` option for minimal output

## 0.1.1

- Validate the length argument as a positive integer
- Hexadecimal mode uses random case when `-a` and `-A` are both omitted or both present
- Added automated tests and password guidance

## 0.1.0

- Always show length in output
- Reverse order of changelog entries (newest first)

## 0.0.5

- Option `-h` renamed to `-x`
- `-h/--help` now available for help output
- Length displayed when using `-r STRING`
- Help shown on parameter errors

## 0.0.4

- Function `generate_password` renamed to `generate_string`
- Calculate and display Shannon and password entropy for generated strings

## 0.0.3

- Option `-c` replaced by positional length argument
- Added `-r STRING` to display Shannon and password entropy of the given string

## 0.0.2

- Project renamed to **stringen**
- Default character set is now `-aAi` when no option is provided
- Added hexadecimal output via `-h`
- Shows Shannon entropy of the generated string

## 0.0.1 - Initial release ("pwgen")

- Command line interface with `-a`, `-A`, `-i`, and `-c` options
- Generates a random string using Python's `secrets` module
