#!/usr/bin/env python
# encoding: utf-8

#############################################################################
# Purpose:
#   Sends a round of personalized newsletters.
#
# Usage:
#   arrr.py
#
# Files:
#   - Expects a file 'user.json' to contain, for each recipient, a field
#     "address" containing the email address and "name" containing a name.
#   - Expects a file 'config.json' with login information for a SMTP mail
#     server, a subject for the mails, and information (name, email address)
#     of the sender.
#   - Expects a directory "mails" that contain a file "header.txt"
#     containing a greeting for the mails, a file "footer.txt" containing
#     a goodbye for the mails, and files "mail1.txt", "mail2.txt", etc.,
#     which will be sent to the users.
#
# Author:
#   Niels Lohmann <niels.lohmann@piraten-mv.de>
#############################################################################


import urllib2

import json

from smtplib import SMTP
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from time import gmtime, strftime, asctime

import dateutil.parser

import locale
import codecs


###########################################################################
# Dectorator to speed up reading from files
###########################################################################

def memoize(function):
  memo = {}
  def wrapper(*args):
    if args in memo:
      return memo[args]
    else:
      rv = function(*args)
      memo[args] = rv
      return rv
  return wrapper


###########################################################################
# Return mail text given the number of the text
###########################################################################

@memoize
def getMailtext(number):
    f = open("mails/mail" + str(number) + ".txt", "r")
    mailtext = f.read()
    f.close()
    return mailtext

@memoize
def getHeader():
    f = open("mails/header.txt", "r")
    mailtext = f.read()
    f.close()
    return mailtext

@memoize
def getFooter():
    f = open("mails/footer.txt", "r")
    mailtext = f.read()
    f.close()
    return mailtext


###########################################################################
# Send email with given content, subject, and address
###########################################################################

def sendMail(content, subject, address, name, config):
    sender = config['sender']['name'] + '<' + config['sender']['address'] + '>'
    recipient = name + ' <' + address + '>'

    msg = MIMEText(content, 'plain', 'UTF-8')
    msg['Subject'] = Header(subject, 'UTF-8')
    msg['From'] = sender
    msg['To'] = Header(recipient.encode('utf-8'), 'UTF-8').encode()

    conn = SMTP(config['smtp']['server'], config['smtp']['port'])
    conn.set_debuglevel(False)
    conn.login(config['smtp']['username'], config['smtp']['password'])

    conn.sendmail(sender, address, msg.as_string())
    conn.close()


###########################################################################
# Read events of the next week
###########################################################################

@memoize
def getEvents():
    # We use a JSON version of our Google calendar. Any other calendar
    # would be fine, too.
    calendar = json.loads(urllib2.urlopen("http://opendata.piratenpartei-mv.de/calendar").read())

    locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

    woche = ""

    for e in calendar:
        if 'date' in e['start']:
            if 'date' in e['end'] and e['start'] == e['end']:
                woche = woche + dateutil.parser.parse(e['start']['date']).strftime("%A, %d.%m.%Y") + "\n"
            else:
                woche = woche + dateutil.parser.parse(e['start']['date']).strftime("%A, %d.%m.%Y") + " bis " + dateutil.parser.parse(e['end']['date']).strftime("%A, %d.%m.%Y") + "\n"
        else:
            woche = woche + dateutil.parser.parse(e['start']['dateTime']).strftime("%A, %d.%m.%Y, %H:%M Uhr") + "\n"
        woche = woche + e['summary'] + " ("
        woche = woche + e['location'] + ")\n\n"
    
    return woche.encode('utf-8')


###########################################################################
# Read the user information and config file
###########################################################################

user = dict()
f = open("user.json", "r")
user = json.load(f)
f.close()

config = dict()
f = open("config.json", "r")
config = json.load(f)
f.close()


###########################################################################
# Prepare and send email
###########################################################################

sent_mails = 0
for entry in user:
    # if no number is given, send the first mail
    if "mailnumber" in entry:
        my_mailnumber = entry['mailnumber']
    else:
        my_mailnumber = 1

    # Format email, replace placeholders - we replace {name} with the
    # field "name" in file "user.json" and {calendarentries} with the
    # week preview generated by getEvents().
    try:
        my_mailtext = getHeader() + getMailtext(my_mailnumber) + getFooter()
        my_mailtext = my_mailtext.format(
            name = entry['name'].encode('utf-8'),
            calendarentries = getEvents()
        )
    except:
        print ("could not send mail #" + str(my_mailnumber) + " to " + entry['address'])
        continue

    sendMail(my_mailtext, config['subject'] + ", Ausgabe " + str(my_mailnumber), entry['address'], entry['name'], config)
    sent_mails = sent_mails + 1

    # store next number and hash of email address
    entry['mailnumber'] = my_mailnumber+1

    if not 'history' in entry:
        entry['history'] = dict()
    entry['history'][my_mailnumber] = asctime()

    print ("mail #" + str(my_mailnumber) + " to " + entry['address'])


###########################################################################
# Store changed user information
###########################################################################

f = codecs.open("user.json", "w+", "utf-8")
json.dump(user, f, sort_keys=True, indent=4, ensure_ascii=False)
f.close()


print ("\nsent " + str(sent_mails) + " mails.")
