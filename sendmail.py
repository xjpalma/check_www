#!/usr/bin/python

#!/usr/bin/python
"""
send an email through gmail
Save this script to send-gmail.py,
place the body of the email in email_message.txt,
and then run:
    python sendmail.py \
            --wait 5 \
            --user user@gmail.com \
            --pass 'myPassword' \
            --to 'recipient1@example.com' --to 'recipient2@example.com'\
            --subject 'this is the email subject' \
            --body message
which means:
    wait 5 minutes
    then send an email from from@gmail.com
    to recipient1@example.com and recipient2@example.com
    with the subject "this is the email subject"
    and the message from email_message.txt
"""

import os
import sys
import optparse
import smtplib
import time

## python 2
#from email.MIMEMultipart import MIMEMultipart
#from email.MIMEText import MIMEText

## python 3
from email.mime.multipart import MIMEMultipart  ## py3
from email.mime.text import MIMEText


def parse_args():
    parser = optparse.OptionParser()

    parser.add_option('-u', '--user', dest='user',
                      default='meteo.ist@gmail.com', help='gmail account')

    parser.add_option('-p', '--pass', dest='password',
                      default='meteo|tecnico', help='gmail password')

    parser.add_option('-b', '--body', dest='body',
                      default=None, help='email message txt')

    parser.add_option('-s', '--subject', dest='subject',
                      default=None, help='email subject')

    parser.add_option('-f', '--from', dest='from_addr',
                      default='meteo@tecnico.ulisboa.pt',
                      help='specify a from address')

    parser.add_option('-t', '--to', dest='to_addr_list',
                      default=[], action='append',
                      help='specify a TO list')

    #parser.add_option('-c', '--cc', dest='cc_addr_list',
    #                  default=[], action='append',
    #                  help='specify a CC list')

    parser.add_option('-w', '--wait', dest='wait',
                      default=None, help='seconds to wait before sending')

    opts, args = parser.parse_args()

    if not opts.user:
        parser.error("specify sender address with --user 'username@gmail.com'")

    if not opts.password:
        parser.error("specify sender's password with --pass 'myPassword'")

    if not opts.body:
        parser.error('specify a text with the message text as --body')

    if not opts.subject:
        parser.error("specify a subject with --subject 'my subject'")

    if not opts.to_addr_list:
        parser.error('specify at least one recipient with --to')

    opts.cc_addr_list = []

    return opts

def create_message2(from_addr, to_addr_list, cc_addr_list, subject, message):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = ', '.join(to_addr_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(message))
    return msg

def create_message(from_addr, to_addr_list, cc_addr_list, subject, message):
    header  = "From: %s\n" % from_addr
    header += "To: %s\n" % ','.join(to_addr_list)
    header += "Cc: %s\n" % ','.join(cc_addr_list)
    header += "Subject: %s\n\n" % subject
    message = header + message
    return message


def send_mail(user, password, from_addr, to_addr_list, cc_addr_list, subject, message, smtpserver='smtp.gmail.com:465'):

    for to_addr in to_addr_list:

        to_list = [to_addr]
        msg = create_message(from_addr, to_list, cc_addr_list, subject, message)

        try:
            server_ssl = smtplib.SMTP_SSL(smtpserver)
            server_ssl.ehlo()
            server_ssl.login(user,password)
            server_ssl.sendmail(from_addr, to_list, msg)
            server_ssl.close()

            print('Sent email to %s' % (', '.join(to_list)))

        except:
            print('Something went wrong...')


def main():
    opts = parse_args()

    if opts.wait is not None:
        now = time.time()
        future = now + (float(opts.wait) * 60.)
        print('waiting %.2f minutes...' % (float(opts.wait)))
        while now < future:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.)
            now = time.time()
        sys.stdout.write('\ndone waiting...\n')

    send_mail(opts.user, opts.password, opts.from_addr, opts.to_addr_list, opts.cc_addr_list, opts.subject, opts.body)

if __name__ == '__main__':
    main()


