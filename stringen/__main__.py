import argparse
import sys
import math
import string
import secrets
from collections import Counter


def parse_args():
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
    parser.add_argument('length', type=int, nargs='?', default=12,
                        help='length of the generated string')
    return parser.parse_args(), parser


def build_charset(args):
    """Build a string of characters based on provided flags."""
    if args.hex:
        if not (args.lower or args.upper):
            args.lower = True
        return string.digits + ("ABCDEF" if args.upper else "abcdef")

    if not (args.lower or args.upper or args.digits):
        args.lower = args.upper = args.digits = True

    charset = ''
    if args.lower:
        charset += string.ascii_lowercase
    if args.upper:
        charset += string.ascii_uppercase
    if args.digits:
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
        print(f"Length: {text_length}")
        print(f"Shannon entropy: {sh_entropy:.2f} bits")
        print(f"Password entropy: {pw_entropy:.2f} bits")
        return
    charset = build_charset(args)
    if not charset:
        parser.error('No character set selected. Use -a, -A, -i or -x')
    result = generate_string(args.length, charset)
    result_length = len(result)
    sh_entropy = shannon_entropy(result)
    pw_entropy = password_entropy(result)
    print(result)
    print(f"Length: {result_length}")
    print(f"Shannon entropy: {sh_entropy:.2f} bits")
    print(f"Password entropy: {pw_entropy:.2f} bits")


if __name__ == '__main__':
    main()
