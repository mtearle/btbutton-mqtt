#! /usr/bin/python2

import evdev
import lifx
import time

COLOR_NORMAL = lifx.color.HSBK(hue=0.0, saturation=0.0, brightness=1.0, kelvin=3500)
COLOR_NIGHT = lifx.color.HSBK(hue=0.0, saturation=0.0, brightness=0.1099870298313878, kelvin=2750)


def button(lights, color):
    devices = lights.get_devices()
    if len(devices) > 0:
        if not devices[0].power or devices[0].color != color:
            for device in devices:
                device.color = color
                time.sleep(0.1)
                device.power = True
        else:
            for device in devices:
                device.power = False

def big_button(lights):
    print "big button pressed"
    button(lights, COLOR_NORMAL)

def small_button(lights):
    print "small button pressed"
    button(lights, COLOR_NIGHT)

def main(argv):
    device = evdev.InputDevice(argv[1])
    device.grab()
    lights = lifx.Client()
    enter_pressed = False
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            event = evdev.categorize(event)
            key_up = event.keystate == evdev.KeyEvent.key_up
            vol_up = event.keycode == 'KEY_VOLUMEUP'
            enter = event.keycode == 'KEY_ENTER'
            if key_up and enter:
                enter_pressed = True
            elif key_up and vol_up:
                lights.discover()
                if enter_pressed:
                    small_button(lights)
                else:
                    big_button(lights)
                enter_pressed = False

def usage():
   print("usage: lifx-remote.py /dev/input/event?")

if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
       main(sys.argv)
   else:
      usage()