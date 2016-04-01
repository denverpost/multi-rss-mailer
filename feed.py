#!/usr/bin/env python
# Given a list of rss feeds, figure out if we have new items in them  since
# the last time we checked
import sys
import argparse
import doctest
import feedparser
import httplib2
import os
from slugify import slugify


class RecentFeed:
    """ Methods for ingesting and publishing RSS feeds.
        >>> rf = RecentFeed()
        >>> rf.get('http://rss.denverpost.com/mngi/rss/CustomRssServlet/36/213601.xml')
        True
        >>> p = rf.parse()
        """

    def __init__(self, args={}):
        self.args = args
        if 'days' in args:
            self.days = args.days

    def get(self, url):
        """ Wrapper for API requests. Take a URL, return a json array.
            #>>> articles = rf.recently()
            >>> url = 'http://rss.denverpost.com/mngi/rss/CustomRssServlet/36/213601.xml'
            >>> args = build_parser([])
            >>> rf = RecentFeed(args)
            >>> rf.get(url)
            True
            >>> p = rf.parse()
            """
        h = httplib2.Http('.tmp')
        (response, xml) = h.request(url, "GET")
        if response['status'] != '200':
            if 'verbose' in self.args and self.args.verbose:
                print("URL: %s" % url)
            raise ValueError("URL %s response: %s" % (url, response.status))
        self.xml = xml
        return True

    def parse(self, xml=None):
        """ Turn the xml into an object.
            """
        if xml is None:
            xml = self.xml
        return feedparser.parse(xml)

    def recently(self):
        """ Return a feedparser entry object for the last X days of feed entries.
            """
        items = []
        for item in self.p.entries:
            dt = datetime.fromtimestamp(mktime(item.published_parsed))
            delta = datetime.today() - dt

            if delta.days > self.days:
                continue
            items.append(item)
            if 'verbose' in self.args and self.args['verbose']:
                print(delta.days, dt)
        self.items = items
        return items

    def url_to_slug(self, url):
        """ Turn a feed url into a string we can use as a filename.
            """
        return slugify(url)

    def check(self, url):
        """ Check each feed to see if there are new items since the last time
            we checked.
            """
        directory = os.path.dirname(os.path.realpath(__file__))
        if not os.path.isdir('%s/feeds' % directory):
            os.mkdir('%s/feeds' % directory)

        slug = self.url_to_slug(self.url)
        return True

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
        >>> print(args.verbose)
        True
        """
    parser = argparse.ArgumentParser(usage='$ python feed.py',
                                     description='Check rss feed(s) for new items.',
                                     epilog='')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true",
                        help="Run doctests, display more info.")
    parser.add_argument("-d", "--days", dest="days", default=0,
                        help="")
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)

    main(args)
