#!/usr/bin/env python
# Given a list of rss feeds, figure out if we have new items in them  since
# the last time we checked
import sys
import argparse
import doctest

class RecentFeed:
    """ Methods for ingesting and publishing RSS feeds.
        >>> rf = RecentFeed()
        >>> rf.get('http://rss.denverpost.com/mngi/rss/CustomRssServlet/36/213601.xml')
        True
        >>> rf.parse()
        """

    def __init__(self, args={}):
        self.args = args
        if 'days' not in self.args:
            self.args['days'] = 0
        self.days = self.args['days']

    def get(self, url):
        """ Wrapper for API requests. Take a URL, return a json array.
            >>> url = 'http://rss.denverpost.com/mngi/rss/CustomRssServlet/36/213601.xml'
            >>> parser = build_parser()
            >>> args = parser.parse_args([url])
            >>> rf = RecentFeed(args)
            >>> rf.get(url)
            True
            >>> rf.parse()
            #>>> articles = rf.recently()
            """
        h = httplib2.Http('.tmp')
        (response, xml) = h.request(url, "GET")
        if response['status'] != '200':
            if 'verbose' in self.args and self.args.verbose:
                print("URL: %s" % url)
            raise ValueError("URL %s response: %s" % (url, response.status))
        self.xml = xml
        return True

    def parse(self):
        """ Turn the xml into an object.
            """
        p = feedparser.parse(self.xml)
        self.p = p
        return p

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
    args = parser.parse_args(args)
    return args

if __name__ == '__main__':
    args = build_parser(sys.argv[1:])

    if args.verbose == True:
        doctest.testmod(verbose=args.verbose)

    main(args)
