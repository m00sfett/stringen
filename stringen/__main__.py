import argparse
import sys
import math
import string
import secrets
from collections import Counter


def positive_int(value: str) -> int:
    """Return a positive integer or raise ``ArgumentTypeError``."""
    try:
        ivalue = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(str(exc))
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("length must be a positive integer")
    return ivalue


def parse_args(arguments=None):
    """Parse command line arguments."""
    class HelpOnErrorParser(argparse.ArgumentParser):
        def error(self, message):
            self.print_help(sys.stderr)
            self.exit(2, f"{self.prog}: error: {message}\n")

    parser = HelpOnErrorParser(description="Simple string generator", add_help=False)
    parser.add_argument('-h', '--help', action='help', help='show this help message and exit')
    parser.add_argument('-a', '--lower', action='store_true',
                        help='include lowercase letters (a-z)')
    parser.add_argument('-A', '--upper', action='store_true',
                        help='include uppercase letters (A-Z)')
    parser.add_argument('-i', '--digits', action='store_true',
                        help='include digits (0-9)')
    parser.add_argument('-x', '--hex', action='store_true',
                        help='output hexadecimal string (uses -a/-A for case)')
    parser.add_argument('-r', '--entropy', metavar='STRING',
                        help='calculate entropies for STRING and exit')
    parser.add_argument('-c', '--clean', action='store_true',
                        help='display only the generated password or entropy')
    parser.add_argument('length', type=positive_int, nargs='?', default=12,
                        help='length of the generated string')
    return parser.parse_args(arguments), parser


def build_charset(args):
    """Return a character set string based on provided flags."""
    if args.hex:
        if args.lower and not args.upper:
            return string.digits + "abcdef"
        if args.upper and not args.lower:
            return string.digits + "ABCDEF"
        return string.digits + "abcdefABCDEF"

    if not (args.lower or args.upper or args.digits):
        use_lower = use_upper = use_digits = True
    else:
        use_lower = args.lower
        use_upper = args.upper
        use_digits = args.digits

    charset = ''
    if use_lower:
        charset += string.ascii_lowercase
    if use_upper:
        charset += string.ascii_uppercase
    if use_digits:
        charset += string.digits
    return charset


def generate_string(length, charset):
    """Generate string of given length from charset using secrets."""
    return ''.join(secrets.choice(charset) for _ in range(length))


def shannon_entropy(text):
    """Return Shannon entropy of the given text."""
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())


def password_entropy(text):
    """Return password entropy based on character set size and length."""
    if not text:
        return 0.0
    hex_chars = set('0123456789abcdefABCDEF')
    if all(c in hex_chars for c in text) and any(c.isalpha() for c in text):
        charset = 16
    else:
        charset = 0
        if any(c.islower() for c in text):
            charset += 26
        if any(c.isupper() for c in text):
            charset += 26
        if any(c.isdigit() for c in text):
            charset += 10
    if charset == 0:
        return 0.0
    return len(text) * math.log2(charset)


def main():
    args, parser = parse_args()
    if args.entropy is not None:
        text_length = len(args.entropy)
        sh_entropy = shannon_entropy(args.entropy)
        pw_entropy = password_entropy(args.entropy)
        if args.clean:
            print(f"{pw_entropy:.2f}")
            return
        print(f"Length: {text_length}")
        print(f"Shannon entropy: {sh_entropy:.2f} bits")
        print(f"Password entropy: {pw_entropy:.2f} bits")
        return
    charset = build_charset(args)
    if not charset:
        parser.error('No character set selected. Use -a, -A, -i or -x')
    result = generate_string(args.length, charset)
    if args.clean:
        print(result)
        return
    result_length = len(result)
    sh_entropy = shannon_entropy(result)
    pw_entropy = password_entropy(result)
    print(result)
    print(f"Length: {result_length}")
    print(f"Shannon entropy: {sh_entropy:.2f} bits")
    print(f"Password entropy: {pw_entropy:.2f} bits")


if __name__ == '__main__':
    main()
