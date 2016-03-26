#!/usr/bin/env python
import smtplib
import argparse
import doctest
from email.mime.text import MIMEText

def send_mail(filename, sender, *recipients):
    """ Send an email with the new items to someone.
        >>> filename = 'mailer.py'
        >>> recipients = ['noreply@denverpost.com']
        >>> sender = 'noreply@denverpost.com'
        >>> send_mail(filename, sender, *recipients)

        """
    fp = open(filename, 'rb')
    msg = MIMEText(fp.read())
    fp.close()

    msg['Subject'] = ''
    msg['From'] = sender
    msg['To'] = recipients[0]

    s = smtplib.SMTP('localhost')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='', description='Email people.',
                                     epilog='')
    parser.add_argument('--sender', dest='sender', action='store',
                        help='The "From" field in the email being sent')
    parser.add_argument("-v", "--verbose", dest="verbose", default=False, action="store_true")
    parser.add_argument("recipients", action="append", nargs="*")
    args = parser.parse_args()

    if args.verbose:
        doctest.testmod(verbose=args.verbose)

    send_mail(filename, args.sender, *args.recipients[0])
