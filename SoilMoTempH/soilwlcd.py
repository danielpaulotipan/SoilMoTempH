import RPi.GPIO as GPIO
import os
import glob
import time
import Adafruit_ADS1x15
import datetime
import lcddriver
import time

#####################################################
#shutdown
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(18,GPIO.OUT)

#List Initial Time
starttime = time.time()

#LCD
display = lcddriver.lcd()

#Temperature Sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#ADC Converter
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 2/3

#File
filename = "/home/pi/soil_data/soil " + "{:%H:%M %m-%d-%Y}".format(datetime.datetime.now()) + ".txt"
file = open(filename, "a")
file.write("Time, Temp, Moisture, pH,")
file.write('\n')

######################################################

#Define temperature Sensor
def Shutdown(channel):
	os.system("sudo cp -a /home/pi/soil_data/. /media/pi/usb1")
	display.lcd_display_string("Good Bye!!!         ", 1)
	display.lcd_display_string("EARTHlab DLSU Manila", 2)
	display.lcd_display_string("{:%Y-%m-%d %H:%M:%S}  ".format(datetime.datetime.now()), 3)
	display.lcd_display_string("Wait for 10 seconds ", 4)
	display.backlight(0)
	time.sleep(3)

	os.system("sudo killall python && sudo shutdown -h now")

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        answer = str(round(temp_c, 2))
	return answer

######################################################u
#Print
GPIO.add_event_detect(4, GPIO.FALLING, callback = Shutdown, bouncetime = 2000)

while True:
	now = datetime.datetime.now()
	time.sleep(60 - now.second - now.microsecond / 1e6)

	while (Shutdown == True):

		GPIO.output(18,GPIO.HIGH)

		values  = [0]*4
		values2 = [1]*4

	        values[0] = adc.read_adc(0, gain=GAIN)
	        vmoi = (values[0] * 0.1875)/ 1000
		vmois = 100 - ((vmoi / 4.8) * 100)
		vmoistperc = float(round((vmois), 2))

		if vmoistperc >= 100:
			vmoistperc = 100
			vmoistperc = str(vmoistper)
		elif vmoistperc <= 0:
			vmoistperc = 0
			vmoistperc = str(vmoistperc)
		else:
			vmoistperc = str(vmoistperc)

		offset2 = 0.3
		values2[1] = adc.read_adc(1, gain=GAIN)
		vsoilp = ((values2[1] * 0.1875) / 1000)*3.5
		vsoilph = str(round((vsoilp - offset2),2))

		display.lcd_display_string("{:%H:%M %m-%d-%Y}".format(datetime.datetime.now()), 1)
		display.lcd_display_string("Soil  pH : {0:>6}".format(vsoilph), 2)
		display.lcd_display_string("Moisture : %s %%" % vmoistperc, 3)
		display.lcd_display_string("Temp degC: %s" % read_temp(), 4)

		file.write("{:%Y-%m-%d %H:%M:%S},".format(datetime.datetime.now()))
		file.write("%s," % read_temp() + "%s," % vmoistperc)
		file.write("{0:>6}".format(vsoilph))
		file.write("\n")
		file.flush()

		GPIO.output(18,GPIO.LOW)

		time.sleep(5.0 - ((time.time() - starttime) % 5.0))
