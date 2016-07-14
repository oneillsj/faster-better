#!/bin/bash

#host=$1

#if [ -z $host ]; then
#    echo "Usage: `basename $0` [HOST]"
#    exit 1
#fi


START=`date +%s`
while [ $(( $(date +%s) - 4500 )) -lt $START ]; do

#while :; do
# bime import hosts
for host in 10.0.102.61 10.0.100.236 10.0.101.112 10.0.101.34 10.0.101.240 10.0.102.10 10.0.102.177 10.0.102.15 10.0.100.129 10.0.101.134 10.0.101.156 10.0.102.173 10.0.102.185 10.0.100.16 10.0.102.100 10.0.101.32 10.0.101.108; do
    result=`ping -W 1 -c 1 $host | grep 'bytes from '`
    if [ $? -gt 0 ]; then
        echo -e "`date +'%Y/%m/%d %H:%M:%S'` - host $host is \033[0;31mdown\033[0m" >> bimeimport_fail_$1.txt
    else
#        echo -e "`date +'%Y/%m/%d %H:%M:%S'` - host $host is \033[0;32mok\033[0m -`echo $result | cut -d ':' -f 2`" # >> success_$1.txt
#        sleep 1 # avoid ping rain
    fi
done

done
