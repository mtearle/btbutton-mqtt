# btbutton-mqtt

Mark Tearle <mark@tearle.com>, July 2017

## README

Based on the github gist available here:
https://gist.github.com/dzamlo/16bc43e20f299e2206659ff0c3b2306b

This script integrates/rewrites to interface the Bluetooth Shutter Buttons with MQTT for use with Home Assistant.


## CONFIG

The script looks for a config file, located in /etc/btbutton.cfg or the same directory as the script.

	[mqtt]
	host = <hostname>
	port = 1883
	user = <username>
	password = <password>
	

## FILES
The full paths of the files are:
- /etc/udev/rules.d/99-btbutton-mqtt.rules
- /etc/systemd/system/btbutton-mqtt@.service
- /usr/local/bin/btbutton-mqtt.py
- /etc/btbutton.cfg

Install the python dependancies lister in requirements.txt using pip.

If you have multiple remotes, you can filter them in the udev rule.

## ACKNOWLEDGEMENTS

* Example code from paho-mqtt website by Roger Light <roger@atchoo.org>
* LiFX Btbutton code by Loïc Damien <loic.damien@dzamlo.ch>

## SEE ALSO

- http://hackaday.com/2016/09/14/hacking-a-dollar-store-bluetooth-device/
- http://troydenton.ca/?p=168
- https://www.hackster.io/AdiK/selfie-blink-control-leds-using-selfie-bluetooth-remote-93558e
- https://shkspr.mobi/blog/2016/02/cheap-bluetooth-buttons-and-linux/
- https://gist.github.com/dzamlo/16bc43e20f299e2206659ff0c3b2306b 
