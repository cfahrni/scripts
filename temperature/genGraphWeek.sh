#/bin/bash

rrdtool graph /home/pi/temperature_week.png \
-w 800 -h 400 -a PNG \
--slope-mode \
--start -604800 --end now \
--vertical-label "Temperatur (°C)" \
--upper-limit 10 \
--lower-limit -30 \
DEF:temp1=/home/pi/temperature.rrd:temp1:MAX \
DEF:temp2=/home/pi/temperature.rrd:temp2:MAX \
LINE1:temp1#3952ee:"Tiefkühler \n" \
LINE1:temp2#415372:"Kühlschrank" \
