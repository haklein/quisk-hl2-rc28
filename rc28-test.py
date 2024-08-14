#!/usr/bin/python3

import hid
import time
import math

product_id=30
vendor_id=3110


for device_dict in hid.enumerate():
    if device_dict['product_string'] == "Icom RC-28 REMOTE ENCODER":
        keys = list(device_dict.keys())
        keys.sort()
        for key in keys:
                print("%s : %s" % (key, device_dict[key]))
    print()

try:
    print("Opening the device")

    h = hid.device()
    h.open(vendor_id, product_id)

    print("Manufacturer: %s" % h.get_manufacturer_string())
    print("Product: %s" % h.get_product_string())
    print("Serial No: %s" % h.get_serial_number_string())

    # enable non-blocking mode
    h.set_nonblocking(1)

    # write some data to the device
    print("Write the data")
    # h.write([0x0, 0x1, 1]) # 00001 bot h orange
    # h.write([0x0, 0x1, 2]) # 00010 transmit red, right orange
    # h.write([0x0, 0x1, 3]) # 00011 only right orange
    # h.write([0x0, 0x1, 4]) # 00100 transmit red, left orange
    # h.write([0x0, 0x1, 5]) # 00101 only left orange
    # h.write([0x0, 0x1, 6]) # 00110 only transmit red
    h.write([0x0, 0x1, 0])
    time.sleep(1);
    h.write([0x0, 0x1, 7])
    # bits for LED seem to be inverted:
    # 110 both orange
    # 101 right orange + TR
    # 100 right orange
    # 011 left orange + TR
    # 010 left orange
    # 001 TR
    # 4th bit is for link status
    time.sleep(0.05)

    # read back the answer
    print("Read the data")
    while True:
        d = h.read(64)
        if len(d)==32:
            if d[0]==1: # valid frame
                if d[3]>0:
                    val = d[1]
                    if d[3]==2:
                        val *= -1
                    print(val)
                    print(val* val)
                else:
                    print (d)
                    if d[5] & 1 ==0:
                        print("PTT")
                    else:
                        print("NO PTT")
            else:
                break
        else:
            continue
            # break

    print("Closing the device")
    h.close()

except IOError as ex:
    print(ex)
    print("You probably don't have the hard-coded device.")
    print("Update the h.open() line in this script with the one")
    print("from the enumeration list output above and try again.")

print("Done")
