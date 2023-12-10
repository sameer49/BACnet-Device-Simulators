# pip install BAC0
# pip install bacpypes
# pip install bokeh
# get site- packages : python3 -m site --user-site
# copy above path to /usr/lib/
# add following code in file -  /usr/lib/site-packages/bacpypes/service/cov.py above line 317
# if self.obj.covIncrement is None:
#             self.obj.covIncrement = 0
# sudo kill -9 $(sudo lsof -t -i:47808)

import sys
sys.path.insert(0,"/usr/lib/site-packages/")

import BAC0
import logging
#BAC0.log_level('debug')
# level being 'debug, info, warning, error'
# or
#BAC0.log_level(log_file=logging.DEBUG, stdout=logging.DEBUG, stderr=logging.CRITICAL)

from time import sleep
from sys import exit
from random import *
from BAC0 import lite
from BAC0.core.devices.local.models import (
    analog_input,
    analog_output,
    binary_output,
    binary_input,
)

sleepTime = 5
log=True

# Check ip address
if len(sys.argv) <= 1:
    print("No IP address provided.")
    print("Ex. python3 bacnet_sim.py 192.168.xxx.xxx")
    exit(0)
else:
    ip_addr = sys.argv[1]

# Default Device ID
if len(sys.argv) <= 2:
    print("No device Id provided using default.")
    deviceId = "101"
else:
    deviceId = sys.argv[2]

# Default Port
if len(sys.argv) <= 2:
    print("No Port provided using default.")
    port = '47808'
else:
    port = sys.argv[3]

print("\nIP :"+ip_addr)
print("Port: "+port)
print("Device: "+deviceId)
print("\n")

# Define device
device = lite(ip=ip_addr, port=port, deviceId=deviceId)

# Define device objects
_new_objects = analog_input(
    instance=10,
    name="AI",       
    properties={
        "units": "degreesCelsius",
        "outOfService": "False",      # Prop. Id 81 - Bool 
        #"statusFlags": "1110"         # Prop. Id 111 - Bits
    
    },
    description="Room one Temperature", # Prop. Id 28 - String
    presentValue=18.0,                  # Prop. Id 85 - Real
)
analog_output(
    instance=10,
    name="AO",
    properties={"units": "degreesCelsius"},
    description="Room one set point",
    presentValue=21,
    relinquish_default=21
)

# Assign objects to device
_new_objects.add_objects_to_application(device)

# Main loop
sleep(5)
print("\nSimulation started for every", sleepTime, "seconds\n")
while True:
    device["AI"].presentValue = randint(1,100)*0.5
    
    # logging into console
    if log:
        print("AI present_value: ", device["AI"].presentValue)
        print("AO present_value: ", device["AO"].presentValue)    
            
    # Wait for next iteration
    sleep(sleepTime)
