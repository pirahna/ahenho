# ahenho
A hen house automation project.

## Tasks:
* open / close door according to a schedule
* shitch light on / off according to a schedule
* remote management using web-interface
* remote monitoring of the temperature

## Implementation:

### hardware
Hardware part based on the Raspberry PI B ver.1,
RTC DS3231, Temperature sensor DS18B20. Device 
functioning as WiFi AP. Wifi implemented with
TL-WN722N USB Wlan stick. This one has RP-SMA
antenna connector which was usefull for taking 
antenna out of the steel case.

some custom hardware was created:
* Power off button.
* Power-ON LED
* Door state sensor
* 8xRelay shied was attached to manage light and motor

## software

basic commands were implemented using python 
and RPi.GPIO. 

The python daemon watching power-off
button state was implemented using python and 
RPi.GPIO.

commands are called by system chron daemon.

chron daemon configuration managed using python 
chrontab module.

backend part of the configuratiuon GUI implemented using
python, flask, nginx

frontend part of the configuration GUI uses JS, 
HTML5 and some common JS modules like jQuery, Bootstrap 
etc.
