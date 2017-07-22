#!/bin/bash

SERVO=2                         # servo number
POS1=78                         # position 1
POS2=228                        # position 2
DELAY=0.1                       # delay between steps
POSFILE=/home/pi/scripts/servo/position

# check if file exists
if [ ! -f $POSFILE ]; then
        echo "$POSFILE not found!"
        exit 1
fi

# read current servo position
POSITION=$(cat $POSFILE)

if [ "$POSITION" = "$POS1" ]; then
        echo "- moving to $POS2 -"
        for (( i=$POSITION; i<=$POS2; i++ ))
                do
                echo $SERVO=$i > /dev/servoblaster
                echo $i > $POSFILE
                sleep $DELAY
        done
else
        echo "- moving to $POS1 -"
        for (( i=$POSITION; i>=$POS1; i-- ))
                do
                echo $SERVO=$i > /dev/servoblaster
                echo $i > $POSFILE
                sleep $DELAY
        done
fi
