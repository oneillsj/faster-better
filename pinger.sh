#!/bin/bash

#host=$1

#if [ -z $host ]; then
#    echo "Usage: `basename $0` [HOST]"
#    exit 1
#fi


START=`date +%s`
while [ $(( $(date +%s) - 4500 )) -lt $START ]; do

#while :; do
# import hosts
for host in 1.1.1.1 2.2.2.2 3.3.3.3; do
    result=`ping -W 1 -c 1 $host | grep 'bytes from '`
    if [ $? -gt 0 ]; then
        echo -e "`date +'%Y/%m/%d %H:%M:%S'` - host $host is \033[0;31mdown\033[0m" >> fail_$1.txt
    else
#        echo -e "`date +'%Y/%m/%d %H:%M:%S'` - host $host is \033[0;32mok\033[0m -`echo $result | cut -d ':' -f 2`" # >> success_$1.txt
#        sleep 1 # avoid ping rain
    fi
done

done
