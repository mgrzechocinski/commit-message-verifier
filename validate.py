import argparse
import sys

from commit_msg_validator import validate


def read_in():
    lines = sys.stdin.readlines()
    return ''.join(lines)


def main():
    parser = argparse.ArgumentParser(description="Validates commit message based on STDIN value",
                                     usage="git show --format='%%B' -s HEAD | python <path_to>/validate.py")
    parser.add_argument('--verbose', '-v', required=False, action='store_true', help="Show read input")
    args = parser.parse_args()

    sys.tracebacklimit = 0

    if args.verbose:
        print("Reading from STDIN (escape with ^D)...")

    lines = read_in()
    if args.verbose:
        print("----------- INPUT ---------------")
        sys.stdout.write(lines)
        sys.stdout.flush()
        print("----------- /INPUT ---------------")
    try:
        validate(lines)
        print("Commit message format is valid.")
    except ValueError as error:
        sys.stderr.write("Commit message format is invalid\n")
        sys.stderr.write("Validation error: %s " % error)
        sys.exit(-1)


if __name__ == '__main__':
    main()
