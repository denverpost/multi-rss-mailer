#!/usr/bin/env python
# Given a list of rss feeds, figure out if we have new items in them  since
# the last time we checked
import sys
import argparse
import doctest

def main(args):
    """ Example usage:
        Describe what we do in this file, then give an example of a command you
        might run on the command line.
        $ python3 feed.py
        """
    pass

def build_parser(args):
    """ A testable method of parsing command-line arguments.
        >>> parser = build_parser(['-v'])
        >>> print args.verbose
        True
        """
    parser = argparse.ArgumentParser(usage='$ python feed.py',
                                     description='Check rss feed(s) for new items.',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true",
                        help="Run doctests, display more info.")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)

    main(args)
