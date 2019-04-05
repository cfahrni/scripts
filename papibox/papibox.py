import subprocess, random, glob, vlc, http.client, urllib, requests
from gpiozero import LED, Button
from signal import pause
from picamera import PiCamera
from time import sleep
from datetime import datetime

# define buttons
left_btn = Button(4, hold_time=5)
middle_btn = Button(2)
right_btn = Button(18, hold_time=5)

# define leds
left_led = LED(17)
middle_led = LED(3)
right_led = LED(27)

# define sound effects
soundeffects = {
    'focus' : '/home/pi/papibox/effects/focus.mp3',
    'shutter' : '/home/pi/papibox/effects/shutter.mp3',
    'freeze' : '/home/pi/papibox/effects/freeze.mp3',
    'unlock' : '/home/pi/papibox/effects/unlock.mp3',
    'startup' : '/home/pi/papibox/effects/startup.mp3',
}

# camera settings
camera = PiCamera()
camera.resolution = (1296, 972)

# initialize camera and wait 2s
camera.start_preview()
sleep(2)

# create vlc instance
vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

def play_soundeffect(player,soundfile):

    # load soundfile into instance
    media = vlc_instance.media_new(soundfile)
    player.set_media(media)

    # wait and let memory buffer fill up
    #sleep(1)

    # play song and wait for playback
    player.play()

def play_sound(btn,led,player,soundfile):

    # enable led
    led.on()

    # load soundfile into instance
    media = vlc_instance.media_new(soundfile)
    player.set_media(media)

    # wait and let memory buffer fill up
    #sleep(1)

    # play song and wait for playback
    player.play()
    sleep(2)

    # disable led
    led.off()

def take_picture(led):

    # enable led
    led.on()

    # take picture and close preview
    camera.capture('/tmp/image.jpg')
    play_soundeffect(player,soundeffects.get("shutter"))

    # disable led
    led.off()

    # send pushover message
    r = requests.post("https://api.pushover.net/1/messages.json",
        data = {
            "token": "XXXX",
            "user": "XXXX",
            "message": "Hallo Papi!"},
        files = {
            "attachment": ("image.jpg", open("/tmp/image.jpg", "rb"), "image/jpeg")}
    )

    # archive the image
    subprocess.call("/home/pi/papibox/upload.sh", shell=True)

    # blink led and cooldown for 20s
    led.blink()
    sleep(20)
    led.off()

# startup complete
play_soundeffect(player,soundeffects.get("focus"))

# assign actions to buttons
left_btn.when_released = lambda : play_sound(left_btn,left_led,player,random.choice(glob.glob("/home/pi/papibox/animals/*.mp3")))
middle_btn.when_pressed = lambda : take_picture(middle_led)
right_btn.when_released = lambda : play_sound(right_btn,right_led,player,random.choice(glob.glob("/home/pi/papibox/music/*.mp3")))

# keep script running
pause()
