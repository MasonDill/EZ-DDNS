WD=$(pwd)
PYTHONPATH=/usr/bin/python3
FILEPATH=$WD/ddns.py
LOGPATH=$WD/ddns.log

#Comment out the options you don't want
VERBOSE="--verbose"
LOG="--log"

#minute hour day month dayofweek
INTERVAL="0 * * * *"

echo "$INTERVAL $PYTHONPATH $FILEPATH --logf $LOGPATH $VERBOSE $LOG" | crontab -