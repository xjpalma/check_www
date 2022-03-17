#!/usr/bin/env python3
"""
send an email through gmail
Save this script to send-gmail.py,
place the body of the email in email_message.txt,
and then run:
    python sendmail.py \
            --wait 5 \
            --user user@gmail.com \
            --pass 'myPassword' \
            --to 'recipient1@example.com' --to 'recipient2@example.com' \
            --subject 'this is the email subject' \
            --body message \
            --att 'attachment_path'
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
import time
import smtplib
from email.message import EmailMessage
import traceback

# For guessing MIME type based on file name extension
import mimetypes
from pathlib import Path

default_email_user = ""
default_email_pass = ""
default_email_from = ""


def parse_args():
    parser = optparse.OptionParser()

    parser.add_option("-u", "--user", dest="user", default=default_email_user, help="gmail account")

    parser.add_option("-p", "--pass", dest="app_password", default=default_email_pass, help="google app password")

    parser.add_option("-b", "--body", dest="body", default=None, help="email message txt")

    parser.add_option("-s", "--subject", dest="subject", default=None, help="email subject")

    parser.add_option("-a", "--att", dest="attachment", default=None, help="path of attachment")

    parser.add_option("-f", "--from", dest="from_addr", default=default_email_from, help="specify a from address")

    parser.add_option("-t", "--to", dest="to_addr_list", default=[], action="append", help="specify a TO list")

    # parser.add_option('-c', '--cc', dest='cc_addr_list',
    #                  default=[], action='append',
    #                  help='specify a CC list')

    parser.add_option("-w", "--wait", dest="wait", default=None, help="seconds to wait before sending")

    opts, args = parser.parse_args()

    if not opts.user:
        parser.error("specify sender address with --user 'username@gmail.com'")

    if not opts.app_password:
        parser.error("specify sender's password with --pass 'myAppPassword'")

    if not opts.body:
        parser.error("specify a text with the message text as --body")

    if not opts.subject:
        parser.error("specify a subject with --subject 'my subject'")

    if not opts.from_addr:
        opts.from_addr = opts.user

    if not opts.to_addr_list:
        parser.error("specify at least one recipient with --to")

    opts.cc_addr_list = []

    return opts


def create_message(from_addr, to_addr_list, cc_addr_list, subject, message, path):
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addr_list)
    msg["Subject"] = subject
    msg.set_content(message)

    # add attachment if exist
    if path:
        try:
            path = Path(path)
            filename = path.name

            # Guess the content type based on the file's extension.  Encoding
            # will be ignored, although we should check for simple things like
            # gzip'd or compressed files.
            ctype, _ = mimetypes.guess_type(str(path))
            ctype = None
            if ctype is None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = "application/octet-stream"
            mime_type, mime_subtype = ctype.split("/", 1)
            with path.open("rb") as fp:
                content = fp.read()
                msg.add_attachment(content, maintype=mime_type, subtype=mime_subtype, filename=filename)

        except Exception:
            print("Something went wrong with attachment:...")
            traceback.print_exc()
            sys.exit()

    return msg


def send_mail(user, password, from_addr, to_addr_list, cc_addr_list, subject, message, attachment, smtpserver="smtp.gmail.com:465"):
    for to_addr in to_addr_list:

        to_list = [to_addr]
        msg = create_message(from_addr, to_list, cc_addr_list, subject, message, attachment)

        try:
            with smtplib.SMTP_SSL(smtpserver) as smtp:
                smtp.login(user, password)  # login gmail account
                smtp.send_message(msg)  # send message
                print("Sent email to %s" % (", ".join(to_list)))
                if attachment:
                    print(" with attachment: %s" % (attachment))

        except Exception:
            print("Something went wrong:...")
            traceback.print_exc()


def main():
    opts = parse_args()

    if opts.wait is not None:
        now = time.time()
        future = now + (float(opts.wait) * 60.0)
        print("waiting %.2f minutes..." % (float(opts.wait)))
        while now < future:
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1.0)
            now = time.time()
        sys.stdout.write("\ndone waiting...\n")

    send_mail(opts.user, opts.app_password, opts.from_addr, opts.to_addr_list, opts.cc_addr_list, opts.subject, opts.body, opts.attachment)


if __name__ == "__main__":
    main()
