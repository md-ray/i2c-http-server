#!/usr/bin/python

import sys
import SocketServer
import SimpleHTTPServer
import re

from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

PORT = 9090

class CustomHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        if None != re.search('/clean', self.path):
            lcd.clear()
            lcd.backlight(lcd.OFF)
            #This URL will trigger our sample function and send what it returns back to the browser
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write("OK") #call sample function here
            return
        if None != re.search('/lcd/*', self.path):
            paraminput = self.path.split('/')[-1].lower().strip()
            if (paraminput == "on"):
                 lcd.backlight(lcd.ON)
            elif (paraminput == "off"):
                lcd.backlight(lcd.OFF)
            elif (paraminput == "red"):
                lcd.backlight(lcd.RED)
            elif (paraminput == "green"):
                lcd.backlight(lcd.BLUE)
            elif (paraminput == "blue"):
                lcd.backlight(lcd.GREEN)

            print "param=",paraminput 
            
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(paraminput) #call sample function here
            return
        if None != re.search('/msg/*', self.path):
            lcd.clear()
            lcd.backlight(lcd.ON)

            param1 = self.path.split('/')[-2].strip()
            param2 = self.path.split('/')[-1].strip()
            lcd.message(param1 + '\n' + param2)
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(param1 + "-" + param2) #call sample function here
        else:
            #serve files, and directory listings by following self.path from
            #current working directory
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

httpd = SocketServer.ThreadingTCPServer(('', PORT),CustomHandler)
httpd.allow_reuse_address = True

print "serving at port", PORT
try:
    httpd.serve_forever()
finally:
    httpd.server_close()

"""
if (len(sys.argv) <= 1):
    print("Argument not complete")
    exit(1)

if (sys.argv[1] == "clean"):
    lcd.clear()
    lcd.backlight(lcd.OFF)
else:
    lcd.clear()
    lcd.backlight(lcd.ON)

print 'Argument=', sys.argv[0]
"""


# Clear display and show greeting, pause 1 sec

# lcd.message("Adafruit RGB LCD\nPlate w/Keypad!")
sleep(1)

"""
# Cycle through backlight colors
col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON   , lcd.OFF)
for c in col:
    lcd.backlight(c)
    sleep(.5)

# Poll buttons, display message & set backlight accordingly
btn = ((lcd.LEFT  , 'Red Red Wine'              , lcd.RED),
       (lcd.UP    , 'Sita sings\nthe blues'     , lcd.BLUE),
       (lcd.DOWN  , 'I see fields\nof green'    , lcd.GREEN),
       (lcd.RIGHT , 'Purple mountain\nmajesties', lcd.VIOLET),
       (lcd.SELECT, ''                          , lcd.ON))
prev = -1
while True:
    for b in btn:
        if lcd.buttonPressed(b[0]):
            if b is not prev:
                lcd.clear()
                lcd.message(b[1])
                lcd.backlight(b[2])
                prev = b
            break
"""