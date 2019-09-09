# -*- coding: utf-8 -*-

import time, rrdtool, os.path, sys
from subprocess import call

# variables
sensorid = "28-00000504c6fc"
rrdfile = "tempirature.rrd"
graph_hour = "tempirature_hour.png"
graph_day = "tempirature_day.png"
graph_week = "tempirature_week.png"

if not os.path.exists(rrdfile):
    ret = rrdtool.create(rrdfile, "--step", "60",
        "DS:temp1:GAUGE:120:-20:50",
        "RRA:AVERAGE:0.5:1:10080")

# change to working dir
os.chdir(sys.path[0])

# read sensor data
sensor_01 = open ("/sys/bus/w1/devices/" + sensorid + "/w1_slave")
sensor_01_hex = sensor_01.read()

# split temperature from hex string
sensor_01 = sensor_01_hex.split ("\n") [1].split(" ") [9]

# convert to float
sensor_01 = float(sensor_01[2:]) / 1000

# print temperatures to stdout
print time.strftime("%c")+"     "+("sensor_01: %s" % (sensor_01))

# update rrd file
ret = rrdtool.update(rrdfile, 'N:%s' % (sensor_01))

# create rrd graph - hour
ret = rrdtool.graph(graph_hour, "-w 400", "-h 150", "-a", "PNG",
"--start", "-3600", "--end", "now",
"--upper-limit", "40", "--lower-limit", "0",
"--title", "Temperature - 1 Hour\\n",
"DEF:temp1="+rrdfile+":temp1:AVERAGE",
"LINE1:temp1#3952ee:Temperatur\\n",
"GPRINT:temp1:LAST:Current Temperature\: \t%2.1lf °C\c",
"GPRINT:temp1:MIN:Lowest Temperature\: \t%2.1lf °C\c",
"GPRINT:temp1:MAX:Highest Temperature\: \t%2.1lf °C\c")

# create rrd graph - day
ret = rrdtool.graph(graph_day, "-w 400", "-h 150", "-a", "PNG",
"--start", "-86400", "--end", "now",
"--upper-limit", "40", "--lower-limit", "0",
"--title", "Temperature - 1 Day\\n",
"DEF:temp1="+rrdfile+":temp1:AVERAGE",
"LINE1:temp1#3952ee:Temperatur\\n",
"GPRINT:temp1:LAST:Current Temperature\: \t%2.1lf °C\c",
"GPRINT:temp1:MIN:Lowest Temperature\: \t%2.1lf °C\c",
"GPRINT:temp1:MAX:Highest Temperature\: \t%2.1lf °C\c")

# create rrd graph - week
ret = rrdtool.graph(graph_week, "-w 400", "-h 150", "-a", "PNG",
"--start", "-604800", "--end", "now",
"--upper-limit", "40", "--lower-limit", "0",
"--title", "Temperature - 1 Week\\n",
"DEF:temp1="+rrdfile+":temp1:AVERAGE",
"LINE1:temp1#3952ee:Temperatur\\n",
"GPRINT:temp1:LAST:Current Temperature\: \t%2.1lf °C\c",
"GPRINT:temp1:MIN:Lowest Temperature\: \t%2.1lf °C\c",
"GPRINT:temp1:MAX:Highest Temperature\: \t%2.1lf °C\c")
