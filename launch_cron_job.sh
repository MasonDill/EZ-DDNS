set -e
WD=$(pwd)
PYTHONPATH=/usr/bin/python3
FILEPATH=$WD/update_dns.py
LOGPATH=$WD/ddns.log

#Comment out the options you don't want
VERBOSE="--verbose"
LOG="--log"
LOGF="--logf $LOGPATH"
PROVIDER="--provider cloudflare"

#minute hour day month dayofweek
INTERVAL="*/5 * * * *"

echo "Performing dry run"
$PYTHONPATH $FILEPATH $LOGF $VERBOSE $LOG $PROVIDER

echo "Installing cron job"
echo "$INTERVAL $PYTHONPATH $FILEPATH $LOGF $VERBOSE $LOG $PROVIDER" | crontab -