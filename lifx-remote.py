#! /usr/bin/python2

import evdev

def button(device, id, key):
    print "device %s id %s key %s" % (device,id,key)

def big_button(device, id):
    button(device, id, "big")

def small_button(device, id):
    button(device, id, "small")

def main(path,description):
    device = evdev.InputDevice(path)
    id = description
    device.grab()
    print device
    print device.info
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            event = evdev.categorize(event)
            key_up = event.keystate == evdev.KeyEvent.key_up
            vol_up = event.keycode == 'KEY_VOLUMEUP'
            enter = event.keycode == 'KEY_ENTER'
	    print event.keystate
            if key_up and enter:
                small_button(device.phys,id)
            elif key_up and vol_up:
                big_button(device.phys,id)
            print "..."

def usage():
   print("usage: lifx-remote.py /dev/input/event?")

if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
       main(sys.argv[1],sys.argv[2])
   else:
      usage()
