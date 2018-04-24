#!/bin/bash

#Run in a cron or a infinite loop to constant execute MTRs and log the results

TIMESTAMP=$(date +%Y%m%d-%H:%M)
find /var/log/mtr/*.log -mtime +3 -exec rm {} \;
mkdir -p /var/log/mtr
mtr -w -s 1400 -r -c 50 -i 0.4 1.1.1.1 > /var/log/mtr/mtr-dub1-$TIMESTAMP.log &
mtr -w -s 1400 -r -c 50 -i 0.4 2.2.2.2 > /var/log/mtr/mtr-euc1-$TIMESTAMP.log &
