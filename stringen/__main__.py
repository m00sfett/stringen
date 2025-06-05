import argparse
import math
import string
import secrets
from collections import Counter


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Simple string generator", add_help=False)
    parser.add_argument('--help', action='help', help='show this help message and exit')
    parser.add_argument('-a', '--lower', action='store_true',
                        help='include lowercase letters (a-z)')
    parser.add_argument('-A', '--upper', action='store_true',
                        help='include uppercase letters (A-Z)')
    parser.add_argument('-i', '--digits', action='store_true',
                        help='include digits (0-9)')
    parser.add_argument('-h', '--hex', action='store_true',
                        help='output hexadecimal string (uses -a/-A for case)')
    parser.add_argument('-c', '--count', type=int, default=12,
                        help='length of the password')
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


def generate_password(length, charset):
    """Generate password of given length from charset using secrets."""
    return ''.join(secrets.choice(charset) for _ in range(length))


def shannon_entropy(text):
    """Return Shannon entropy of the given text."""
    if not text:
        return 0.0
    freq = Counter(text)
    length = len(text)
    return -sum((count / length) * math.log2(count / length) for count in freq.values())


def main():
    args, parser = parse_args()
    charset = build_charset(args)
    if not charset:
        parser.error('No character set selected. Use -a, -A, -i or -h')
    password = generate_password(args.count, charset)
    entropy = shannon_entropy(password)
    print(password)
    print(f"Entropy: {entropy:.2f} bits")


if __name__ == '__main__':
    main()
