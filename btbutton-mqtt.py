#! /usr/bin/python2


# Includes example code from paho-mqtt website by:

# Copyright (c) 2010,2011 Roger Light <roger@atchoo.org>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 3. Neither the name of mosquitto nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import mosquitto
import os
 
# Define event callbacks
def on_connect(mosq, obj, rc):
    print("rc: " + str(rc))

def on_message(mosq, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_log(mosq, obj, level, string):
    print(string)


import evdev
import ConfigParser

def send_mqtt_message(config, topic, message):
    host = config.get('mqtt','host')
    port = config.get('mqtt','port')
    user = config.get('mqtt','user')
    password = config.get('mqtt','password')

    mqttc = mosquitto.Mosquitto()

    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Uncomment to enable debug messages
    #mqttc.on_log = on_log

    # Connect
    mqttc.username_pw_set(user, password)
    mqttc.connect(host, port)

    # Start subscribe, with QoS level 0
    mqttc.subscribe(topic, 0)

    # 
    # Publish a message
    mqttc.publish(topic, message)

    mqttc.disconnect()


def button(config, device, id, key):
    print "device %s id %s key %s" % (device,id,key)

    topic = "homeassistant/binary_sensor/btbutton/%s_%s/state" % (id,key)
    payload = "ON"
    send_mqtt_message(config,topic,payload)
    payload = "OFF"
    send_mqtt_message(config,topic,payload)


def big_button(config, device, id):
    button(config, device, id, "big")

def small_button(config, device, id):
    button(config, device, id, "small")

def main(path,description):
    # load mqtt config (host, port, user, password)
    config = ConfigParser.ConfigParser()
    config.read(['/etc/btbutton.cfg','btbutton.cfg'])
    #

    # send mqtt discovery for homeassistant

    payload = '{"name":"btbutton", "device_class":"motion"}'
    topic = "homeassistant/binary_sensor/btbutton/%s_big/config" % (description)
    send_mqtt_message(config,topic,payload)
    topic = "homeassistant/binary_sensor/btbutton/%s_small/config" % (description)
    send_mqtt_message(config,topic,payload)
    #

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
                small_button(config, device.phys,id)
            elif key_up and vol_up:
                big_button(config, device.phys,id)
            print "..."

def usage():
   print("usage: btbutton-mqtt.py </dev/input/event?> <description>")

if __name__ == '__main__':
   import sys
   if len(sys.argv) > 1:
       main(sys.argv[1],sys.argv[2])
   else:
      usage()

