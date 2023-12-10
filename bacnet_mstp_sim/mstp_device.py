#!/usr/bin/env python

"""
for enabling COV
add ChangeOfValueServices class to application on line no. 498
/home/$USER/.local/lib/python3.8/site-packages/misty/mstplib/__init__.py

"""

from __future__ import absolute_import
from bacpypes.debugging import ModuleLogger
from bacpypes.consolelogging import ConfigArgumentParser
from bacpypes.core import run
from bacpypes.task import RecurringTask
from bacpypes.primitivedata import Date
from misty.mstplib import MSTPSimpleApplication
from bacpypes.service.cov import ChangeOfValueServices
from bacpypes.service.object import ReadWritePropertyMultipleServices
from bacpypes.object import register_object_type
from bacpypes.local.device import (
    LocalDeviceObject,
)
from bacpypes.local.object import (
    AnalogOutputCmdObject,
    AnalogValueCmdObject,
    BinaryOutputCmdObject,
    BitStringValueCmdObject,
    CharacterStringValueCmdObject,
    LargeAnalogValueCmdObject,
    DateValueCmdObject
)

from random import *
from time import sleep

# globals
AO1 = None
AV1 = None

# some debugging
_debug = 1

# register the classes
v_id = 999
register_object_type(LocalDeviceObject, vendor_id=v_id)
register_object_type(AnalogOutputCmdObject, vendor_id=v_id)
register_object_type(AnalogValueCmdObject, vendor_id=v_id)
register_object_type(BinaryOutputCmdObject, vendor_id=v_id)
register_object_type(BitStringValueCmdObject, vendor_id=v_id)
register_object_type(CharacterStringValueCmdObject, vendor_id=v_id)
#register_object_type(LargeAnalogValueCmdObject, vendor_id=v_id)
#register_object_type(DateValueCmdObject, vendor_id=v_id)

class DoSomething(RecurringTask):
    def __init__(self, interval):
        if _debug:
            print("\nGenerating data every", interval , "seconds")
        RecurringTask.__init__(self, interval * 1000)

        # save the interval
        self.interval = interval

        
    def process_task(self):
        global AO1, AV1
        random_AO1 = randint(1,100)*0.5
        if _debug:
            print("- AO1 presentValue: ", random_AO1, ", - AV1 presentValue: ", AV1.presentValue)
            

        # change the point
        AO1.presentValue = random_AO1
        

def main():
    global this_application, AO1, AV1
    
    # parse the command line arguments
    args = ConfigArgumentParser(description=__doc__).parse_args()

    interval = int(args.ini.interval)
    
    if _debug:
        print("initialization")
    if _debug:
        print("args:\n", args)

    # make a device object
    mstp_args = {
        '_address': int(args.ini.address),
        '_interface':str(args.ini.interface),
        '_max_masters': int(args.ini.max_masters),
        '_baudrate': int(args.ini.baudrate),
        '_maxinfo': int(args.ini.maxinfo),
    }
    # make a device object
    mstp_device = LocalDeviceObject(ini=args.ini, **mstp_args)
    if _debug:
        print("\nmstp_device: %r", mstp_device)
        
    # make a sample application
    this_application = MSTPSimpleApplication(mstp_device, args.ini.address)
    
    # make a commandable analog output object, add to the device (id=1)
    AO1 = AnalogOutputCmdObject(
        objectIdentifier=("analogOutput", 1), 
        objectName="AO1",
        presentValue=6.5, 
        covIncrement=1.0
    )
    if _debug:
        print("\nAdding AO1 object to device: ", AO1)
        print("    - AO1 presntValue: ", AO1.presentValue)
    this_application.add_object(AO1)

    # make a commandable analog value object, add to the device (id=2)
    AV1 = AnalogValueCmdObject(
        objectIdentifier=("analogValue", 1), 
        objectName="AV1",
        presentValue=5.5, 
        covIncrement=1.0
    )
    if _debug:
        print("\nAdding AV1 object to device: ", AV1)
        print("    - AV1 presntValue: ", AV1.presentValue)
    this_application.add_object(AV1)

    # make a commandable bit string value object, add to the device (id=39)
    BSV1 = BitStringValueCmdObject(
        objectIdentifier=("bitstringValue", 1), 
        objectName="BSV1",
        presentValue="11001", 
    )
    if _debug:
        print("\nAdding BSV1 object to device: ", BSV1)
        print("    - BSV1 presntValue: ", BSV1.presentValue)
    this_application.add_object(BSV1)

    # make a commandable character string value object, add to the device (id=40)
    CSV1 = CharacterStringValueCmdObject(
        objectIdentifier=("characterstringValue", 1), 
        objectName="CSV1",
        presentValue="abcXYZ", 
    )
    if _debug:
        print("\nAdding CSV1 object to device: ", BSV1)
        print("    - CSV1 presntValue: ", CSV1.presentValue)
    this_application.add_object(CSV1)

    # make a commandable binary output object, add to the device (id=4)
    BO1 = BinaryOutputCmdObject(
        objectIdentifier=("binaryOutput", 1),
        objectName="BO1",
        presentValue="Inactive",
    )
    if _debug:
        print("\nAdding BO1 object to device: ", BO1)
        print("    - BO1 presntValue: ", BO1.presentValue)
    this_application.add_object(BO1)

    if _debug:
        print("\nObject list: \n")
        for objects in mstp_device.objectList:
            print(objects)

    do_something_task = DoSomething(interval)
    do_something_task.install_task()

    if _debug:
        print("\nRunning...\n")

    run()

if __name__ == "__main__":
    main()
