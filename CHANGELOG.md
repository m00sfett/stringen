# Changelog

## 0.0.1 - Initial release
- Command line interface with `-a`, `-A`, `-i`, and `-c` options
- Generates a random string using Python's `secrets` module

## 0.0.2
- Project renamed to **stringen**
- Default character set is now `-aAi` when no option is provided
- Added hexadecimal output via `-h`
- Shows Shannon entropy of the generated string

## 0.0.3
- Option `-c` replaced by positional length argument
- Added `-r STRING` to display Shannon and password entropy of the given string
