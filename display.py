#! /usr/bin/python
#Written By Tom Paulus, @tompaulus, www.tompaulus.com

from lib.Char_Plate.Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import socket
import fcntl
import struct
import time
import smbus


lcd = Adafruit_CharLCDPlate(busnum=0)
lcd.clear()
lcd.backlight(lcd.ON)
ip = None
interface = 0


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


while ip is None and interface <= 10:
    try:
        ip = get_ip_address('eth0' + str(interface))
    except IOError:
        pass

    try:
        ip = get_ip_address('wlan' + str(interface))
    except IOError:
        pass
    interface += 1

if ip is not None:
    lcd.message('My IP address is:\n' + get_ip_address('wlan0'))

else:
    lcd.backlight(lcd.RED)
    lcd.message("It seems that I\ndon't have an IP")

while not lcd.buttonPressed(lcd.SELECT):
    time.sleep(.1)

lcd.clear()
lcd.backlight(lcd.OFF)