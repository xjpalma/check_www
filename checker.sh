#!/bin/bash

GMAIL_USER=""
GMAIL_PASS=""

# list of websites. each website in new line. leave an empty line in the end.
SITESLIST=websites.lst

# Send mail in case of failure to. leave an empty line in the end.
EMAILLIST=emails.lst

# `Quiet` is true when in crontab; show output when it's run manually from shell.
# Set THIS_IS_CRON=1 in the beginning of your crontab -e.
# else you will get the output to your email every time
if [ -n "$THIS_IS_CRON" ]; then QUIET=true; else QUIET=false; fi

OK="\e[32m[ok]\e[0m"
NOK="\e[31m[DOWN]\e[0m"

arrVar=()

function test {
  now=$(date)

  response=$(curl --write-out %{http_code} --silent --output /dev/null $1)
  site=$(echo $1 | cut -f1 -d"/")

  if [ "$QUIET" = false ]; then
    echo -n "$now  $site "
  fi

  if echo "$response" | grep -w "200\|301\|302" >/dev/null; then
    # website working
    if [ "$QUIET" = false ]; then
      echo -n "$response "
      echo -e $OK
    fi
    # remove .temp file if exist.
    if [ -f down/$site ]; then rm -f down/$site; fi

  else
    # website down
    if [ "$QUIET" = false ]; then
      echo -n "$response "
      echo -e $NOK
    fi

    DIFF=0
    if [ -f down/$site ]; then
      lastUpdate="$(stat -c %Y down/$site)"
      now="$(date +%s)"
      let DIFF="${now}-${lastUpdate}"
    fi

    if [ ! -f down/$site ] || [ $DIFF -gt 3600 ]; then
      mkdir -p down
      arrVar+=($site)
      echo >down/$site
    fi
  fi
}

## main loop
while read s; do
  if [ -z $s ]; then
    continue
  else
    test $s
  fi
done <$SITESLIST

## crontab
#THIS_IS_CRON=1
#*/30 * * * * /path/to/isOnline/checker.sh
if [[ "${#arrVar[@]}" > 0 ]]; then
  while read e; do
    if [ -z "${e}" ]; then
      continue
    else
      ## using python sendmail command
      body="${#arrVar[@]} websites down:"
      for v in "${arrVar[@]}"; do
        body="$body
 $v"
      done
      python sendmail.py --user $GMAIL_USER --pass $GMAIL_PASS -f $GMAIL_USER -t $e -s 'WEBSITE DOWN' -b "$body"
    fi
  done <$EMAILLIST

fi
