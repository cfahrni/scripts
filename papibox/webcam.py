# import libraries
from gpiozero import LED, Button
from picamera import PiCamera
from time import sleep
from datetime import datetime
import http.client, urllib, requests
from pygame import mixer
import subprocess

# init sound
mixer.init()
focus = mixer.Sound('/home/pi/focus.wav')
shutter = mixer.Sound('/home/pi/shutter.wav')

# camera settings
camera = PiCamera()
camera.resolution = (1296, 972)

# define inputs
trigger = Button(2)
led = LED(3)

# disable led
led.off()


# add keyboard interrupt
try:
        while True:
                # wait for trigger
                trigger.wait_for_press()

                # initialize camera and wait 2s
                camera.start_preview()
                focus.play()
                sleep(2)

                # take picture and close preview
                shutter.play()
                led.on()
                camera.capture('/tmp/image.jpg')
                camera.stop_preview()
                led.off()

                # send pushover message
                r = requests.post("https://api.pushover.net/1/messages.json", data = {
                  "token": "XXXXXXXXXXXXXXXXXXXXXXXXX",
                  "user": "XXXXXXXXXXXXXXXXXXXXXXXXX",
                  "message": "Hallo Papi!"
                },
                files = {
                  "attachment": ("image.jpg", open("/tmp/image.jpg", "rb"), "image/jpeg")
                })

                # archive the image
                subprocess.call("/home/pi/upload.sh")

                # cooldown for 20s
                for x in range (0,19):
                    led.off()
                    sleep(1)
                    led.on()
                    sleep(1)

                # disable led
                led.off()

except KeyboardInterrupt:
        print('Exit.')
