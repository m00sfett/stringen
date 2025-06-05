# Changelog
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

## 0.0.1 - Initial release
- Command line interface with `-a`, `-A`, `-i`, and `-c` options
- Generates a random string using Python's `secrets` module
