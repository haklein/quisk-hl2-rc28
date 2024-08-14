# quisk-hl2-rc28
Quisk hardware file for a Hermes Lite 2 controlled by an ICOM RC-28 remote encoder

Likely requires an udev rule like this for non-root access:
~~~
SUBSYSTEM=="usb", ATTR{product}=="Icom RC-28 REMOTE ENCODER", MODE="0666"
~~~
