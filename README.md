# check_www

[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

check_www is a bash script to check if a list of sites are online. Send a mail if not

# Features

-   use sendmail.py, a python script to send emails
-   use a list of url to check if is sites are online
-   use a list of emails to send message in case of failure

# Tech

check_www is written in bash and use a Python version 3 to send email.

## Installation

check_www runs on linux and requires bash and [Python](https://www.python.org) v3+ to run. You need a gmail account to send email. In checker.sh file fill _GMAIL_USER_ and _GMAIL_PASS_ with your gmail account credentials To run it, open your favorite Terminal and type these commands. Replace <dir_to_install> to you instalation directory

```sh
$ cd <dir_to_install>
$ git clone https://github.com/xjpalma/check_www.git
$ cd check_www
```

-   open checker.sh and fill _GMAIL_USER_ and _GMAIL_PASS_ with your gmail account credentials
-   open _websites.lst_ and list each website in new line. Leave an empty line in the end
-   open _emails.lst_ and list all emails to send message in case of failure. Leave an empty line in the end

```
$ ./checker.sh
```

# License

MIT **Free Software, Hell Yeah!**
