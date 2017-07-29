# README

Based on the github gist available here:
https://gist.github.com/dzamlo/16bc43e20f299e2206659ff0c3b2306b

This script integrates/rewrites to interface the Bluetooth Shutter Buttons 
with MQTT.


# FILES


The full paths of the file are:
/etc/udev/rules.d/99-lifx-keyboard.rules
/etc/systemd/system/lifx-remote@.service
/usr/local/bin/lifx-remote.py

Install the python dependancies lister in requirements.txt using pip.

If you have multiple remote, you could filter them in the udev rule.
It should work with multiple bulb, but I haven't tested that.

# ACKNOWLEDGEMENTS



# SEE ALSO

http://hackaday.com/2016/09/14/hacking-a-dollar-store-bluetooth-device/
http://troydenton.ca/?p=168
https://www.hackster.io/AdiK/selfie-blink-control-leds-using-selfie-bluetooth-remote-93558e
https://shkspr.mobi/blog/2016/02/cheap-bluetooth-buttons-and-linux/



