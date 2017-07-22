# imports
import time
import rrdtool
from subprocess import call

# read sensor data
sensor_freezer = open ("/sys/bus/w1/devices/28-0000042ea895/w1_slave")
sensor_freezer_hex = sensor_freezer.read()

sensor_fridge = open ("/sys/bus/w1/devices/28-00000504c6fc/w1_slave")
sensor_fridge_hex = sensor_fridge.read()

# split temperature from hex string
sensor_freezer = sensor_freezer_hex.split ("\n") [1].split(" ") [9]
sensor_fridge = sensor_fridge_hex.split ("\n") [1].split(" ") [9]

# convert to float
freezer_temperature = float(sensor_freezer[2:]) / 1000
fridge_temperature = float(sensor_fridge[2:]) / 1000

# print temperatures to stdout
print time.strftime("%c")+"     "+("Freezer: %s Fridge: %s" % (freezer_temperature, fridge_temperature))

# update rrd graphs
ret = rrdtool.update('/home/pi/temperature.rrd', 'N:%s:%s' % (freezer_temperature,fridge_temperature))

# push alert on high temperature
if (fridge_temperature > 7 ) :
        call(['/home/pi/scripts/pushover/pushover.sh', '-t','"fridge"', ("Kuehlschrank-Temperatur: %f" % (fridge_temperature))])

if (freezer_temperature > -15 ) :
        call(['/home/pi/scripts/pushover/pushover.sh', '-t','"fridge"', ("Gefrierfach-Temperatur: %f" % (freezer_temperature))])
