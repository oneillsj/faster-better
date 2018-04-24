#!/bin/bash

date=$(TZ=UTC date '+%Y-%m-%d %H:%M')

## Defined hosts which you want ping tests to be executed from
#Dub
dub=admin1.dub1
#fra
fra7=admin1.pod7
fra11=admin1.pod11
#iad
iad5=admin1.pod5
iad6=admin1.pod6
iad9=admin1.pod9
#sac
sac2=admin1.pod2
sac4=admin1.pod4
sac8=admin1.pod8
#NET-01



printf "UTC - Date/Time : $date\n"
#ssh  $dub3 "'ping -q -c 10 $iad5'"

#ssh -q -t $dub "printf '$dub >> $iad5\n'; ping -q -c 10 $iad5 | egrep 'packets|rtt'; printf '\ntesting\n'" &
#ssh -q -t $iad5 "printf '$iad5 >> $dub\n'; ping -q -c 10 $dub | egrep 'packets|rtt'" &
#ssh -q -t $iad5 "printf '$iad5 >> $sac2\n'; ping -q -c 10 $sac2 | egrep 'packets|rtt'" &
#ssh -q -t $sac2 "printf '$sac2 >> $iad5\n'; ping -q -c 10 $iad5 | egrep 'packets|rtt'" 

printf "\nDUB >> IAD|SAC|FRA\n"
fcmd=$(ssh -q -t $dub "ping -q -c 10 $iad5;");origcmd1=$(echo "$fcmd" | egrep "packets|rtt");printf "$dub >> $iad5\n"; echo "${origcmd1}" 
fcmd=$(ssh -q -t $dub "ping -q -c 10 $sac4");origcmd2=$(echo "$fcmd" | egrep "packets|rtt");printf "$dub >> $sac4\n"; echo "${origcmd2}" 
fcmd=$(ssh -q -t $dub "ping -q -c 10 $fra7");origcmd3=$(echo "$fcmd" | egrep "packets|rtt");printf "$dub >> $fra7\n"; echo "${origcmd3}" 

printf "\nIAD >> DUB|SAC|FRA\n"
fcmd=$(ssh -q -t $iad5 "ping -q -c 10 $dub");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$iad5 >> $dub\n"; echo "${origcmd4}" 
fcmd=$(ssh -q -t $iad5 "ping -q -c 10 $sac4");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$iad5 >> $sac4\n"; echo "${origcmd4}" 
fcmd=$(ssh -q -t $iad5 "ping -q -c 10 $fra7");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$iad5 >> $fra7\n"; echo "${origcmd4}" 

printf "\nSAC >> DUB|IAD|FRA\n"
fcmd=$(ssh -q -t $sac4 "ping -q -c 10 $dub");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$sac4 >> $dub\n"; echo "${origcmd4}" 
fcmd=$(ssh -q -t $sac4 "ping -q -c 10 $iad5");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$sac4 >> $iad5\n"; echo "${origcmd4}" 
fcmd=$(ssh -q -t $sac4 "ping -q -c 10 $fra7");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$sac4 >> $fra7\n"; echo "${origcmd4}" 

printf "\nFRA >> DUB|IAD|SAC\n"
fcmd=$(ssh -q -t $fra7 "ping -q -c 10 $dub");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$fra7 >> $dub\n"; echo "${origcmd4}" 
fcmd=$(ssh -q -t $fra7 "ping -q -c 10 $iad5");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$fra7 >> $iad5\n"; echo "${origcmd4}" 
fcmd=$(ssh -q -t $fra7 "ping -q -c 10 $sac4");origcmd4=$(echo "$fcmd" | egrep "packets|rtt");printf "$fra7 >> $sac4\n"; echo "${origcmd4}" 

#echo $dub
#echo $iad5
# result=$(ssh -q -t $dub "ping -q -c 10 $iad5 | egrep '10 packets'" &)
# result2=$(ssh -q -t $iad5 "ping -q -c 10 $dub | egrep 'rtt'" &)
# result3=$(ssh -q -t $iad5 "ping -q -c 10 $sac2 | egrep 'rtt'" &)
# result4=$(ssh -q -t $sac2 "ping -q -c 10 $iad5 | egrep 'rtt'" &)
# echo $result &
# echo $result2 &
# echo $result3 &
# echo $result4

