import argparse
import string
import secrets


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Simple password generator")
    parser.add_argument('-a', '--lower', action='store_true',
                        help='include lowercase letters (a-z)')
    parser.add_argument('-A', '--upper', action='store_true',
                        help='include uppercase letters (A-Z)')
    parser.add_argument('-i', '--digits', action='store_true',
                        help='include digits (0-9)')
    parser.add_argument('-c', '--count', type=int, default=12,
                        help='length of the password')
    return parser.parse_args(), parser


def build_charset(args):
    """Build a string of characters based on provided flags."""
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


def main():
    args, parser = parse_args()
    charset = build_charset(args)
    if not charset:
        parser.error('No character set selected. Use -a, -A, or -i')
    password = generate_password(args.count, charset)
    print(password)


if __name__ == '__main__':
    main()
