#!/usr/bin/python3 

from collections import Counter
import argparse
import re

fromMail = []


class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'


def findMail(file):
    read = open(file, 'r')
    content = read.readlines()
    for i in content:
        email = re.findall(r'from\=\<[a-zA-Z._-]+@[a-zA-Z]+\.(?:[a-zA-Z\.a-zA-Z]+)>\sto=', i)
        if len(email) > 0:
            fromMail.append(email[0].split()[0].split('<')[1].replace('>', ''))


def readWhitelist(whitelist):
    with open(whitelist, 'r') as f:
        content = f.read().splitlines()
        return content


my_parser = argparse.ArgumentParser(description='List of options')
my_parser.add_argument('--file', '-f', type=str, help='locaton of mail.log', default='/var/log/mail.log')
my_parser.add_argument('--send', '-s', type=int, help='number of send mail', required=True)
my_parser.add_argument('--whitelist', '-l', type=str, help='locaton of whitelist')
args = vars(my_parser.parse_args())

print('Filter: {}'.format(args['file']))

findMail(args['file'])
counterMail = Counter(fromMail)
if fromMail:
    for email in counterMail:
        if counterMail.get(email) >= args['send']:
            if args['whitelist']:
                whitelistRead = readWhitelist(args['whitelist'])
                if email in whitelistRead:
                    print('{}: {} - Listed in Whitelist'.format(email, counterMail.get(email)))
                else:
                    print('{}: {}{} - DANGER{}'.format(email, color.RED, counterMail.get(email), color.END))
            else:
                print('{}: {}{}{}'.format(email, color.RED, counterMail.get(email), color.END))