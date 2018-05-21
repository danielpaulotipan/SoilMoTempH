#!/usr/bin/python
import sys
import datetime
import time
import serial
from Tkinter import *
import tkFont as tkfont
import ttk
import os
import glob
import g3
import sys
import RPi.GPIO as GPIO
import pycurl
import time
from StringIO import StringIO
from struct import *
debug=1

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Serial port parameters Arduino Mega
serial_speed = 9600
serial_port = '/dev/ttyACM0'
ser = serial.Serial(serial_port, serial_speed)
ser.flushInput()

# Serial port parameters Arduino Uno
serial_speed2 = 9600
serial_port2 ='/dev/ttyUSB0'
ser2 = serial.Serial(serial_port2, serial_speed2)
ser2.flush

#Filename
filename = "/home/pi/Desktop/AQMS(" + "{:%H_%M %Y_%m_%d})".format(datetime.datetime.now()) + ".txt"
file = open(filename, "w")
file.write(Time,PM1,PM2.5,PM10,Temp,Hum,NO2,O3,CO2,SO2,CO)

air=g3.g3sensor()

SERVER_URL = "http://weather.pogznet.com/"
API_ENDPOINT = "data_add?"
SEID = "6"	
SKEY = "b013aqd2"
BASE_URL = SERVER_URL+API_ENDPOINT \
	+ "seid=" + SEID \
	+ "&skey=" + SKEY
DRYRUN = False
VAL_time = str(int(time.time()))
############################################################## Main Tkinter application #######################################################

class Application(Frame):

########################## Measure data from the sensor
	def measure(self):
		# Request data and read the answer
		ser.write("m")
		time.sleep(.1)
		data = ser.readline()

		ser2.write("m")
		time.sleep(.1)
		data2 = ser2.readline()

		try:
			pmdata=air.read("/dev/ttyAMA0") #pms3003
		except:
			pmdata=[0,0,0,0,0,0]

		# If the answer is not empty, process & display data
		try:
			data = data.strip('\r\n')
			processed_data = data.split(",")

			data2 = data2.strip('\r\n')
			processed_data2 = data2.split(",")

			x = pmdata[3]
			y = pmdata[5]
			z = pmdata[4]

			try:
#				print(str(processed_data))
				file.write("{:%Y_%m_%d %H_%M_%S},".format(datetime.datetime.now()))
				file.write(str(x) + "," + str(y) + "," + str(z) + ",")
				file.write(str(processed_data[0]) + ","
				 + str(processed_data[1]) + ","
				 + str(processed_data[2]) + ","
				 + str(processed_data[3]) + ","
				 + str(processed_data[4]) + ","
				 + str(processed_data2[0]) + ","
				 + str(processed_data2[1])
                         	 )
				file.write("\r\n")
				file.flush()

			except(IndexError, ValueError):
				data = "null"
				
			try:
				HTTP_REQUEST = BASE_URL + "&time=" + VAL_time \
					+ "&pm01=" + str(x) \
					+ "&pm25=" + str(y) \
					+ "&pm10=" + str(z) \
					+ "&temp=" + processed_data[0] \
					+ "&humi=" + processed_data[1] \
					+ "&no2x=" + processed_data[2] \
					+ "&ozne=" + processed_data[3] \
					+ "&co2x=" + processed_data[4] \
					+ "&so2x=" + processed_data2[0] \
					+ "&coxx=" + processed_data2[1]
					
				sendbuff = StringIO()
				s = pycurl.Curl()
				s.setopt(c.URL, HTTP_REQUEST)
				s.setopt(c.WRITEDATA, sendbuff)
				s.perform()
				s.close()
					
				req_result = sendbuff.getvalue()

				print curr_time + " - " + req_result
	
	            # For logging purposes
	            f = open('/home/pi/aggregator.log', 'a')
				f.write(curr_time + " - " + req_result + "\n")
				f.close()
				
			except(IndexError, ValueError):
				data = "null"

			self.time_data.set("Time: {:%H:%M} ".format(datetime.datetime.now()))
			self.date_data.set("Date: {:%Y-%m-%d} ".format(datetime.datetime.now()))

			self.temp_data.set("Temp: " + str(processed_data[0] + " degC"))
			self.hum_data.set("Humidity: " + str(processed_data[1] + " %"))
			self.no2_data.set("NO2: " + str(processed_data[2] +" ppm"))
			self.o3_data.set("O3: " + str(processed_data[3] + " ppm"))
			self.co2_data.set("CO2: " + str(processed_data[4] + " ppm"))

			self.so2_data.set("SO2: " + str(processed_data2[0] + " ppm"))
			self.co_data.set("CO: " + str(processed_data2[1] + " ppm"))

			self.pm1_data.set ("PM1: "   + str(x) + " ug/m3")
			self.pm25_data.set("PM2.5: " + str(y) + " ug/m3")
			self.pm10_data.set("PM10: "  + str(z) + " ug/m3")

		except(IndexError, ValueError):
			data = "null"

        	# Wait 1 second between each measurement
                self.after(1000,self.measure)

############################################################## FILEWRITE ##################################################################



############################ Create display elements ######################################################################################
	def createWidgets(self):

		#PM FRAME
		self.Frame1 = Frame(self, bg="gray7", borderwidth=10, height=200)
		self.Frame1.grid( row=0, column=0, rowspan=3, columnspan=2, sticky=W+E+N+S, padx=2, pady=2)

		#Temp FRAME
		self.Frame2 = Frame(self, bg="gray15", borderwidth=10, height=200)
                self.Frame2.grid( row=3, column=0, rowspan=3, columnspan=2, sticky=W+E+N+S, padx=2, pady=2)

		#Gas FRAME
		self.Frame3 = Frame(self, bg="gray37", borderwidth=10, height=300)
                self.Frame3.grid( row=0, column=2, rowspan=4, columnspan=3, sticky=W+E+N+S, padx=2, pady=2)

		#Time Frame
		self.Frame4 = Frame(self, bg="gray50", borderwidth=10, height=40)
		self.Frame4.grid( row=4, column=2, rowspan=4, columnspan=3, sticky=W+E+N+S, padx=2, pady=2)

############################################################### FRAME1

		self.pm = Label(self.Frame1, width=21, height=2, text="Particulate Matter", bg="gray7", fg="bisque", font=('Verdana', 20, 'italic'))
		self.pm.grid(pady=2)
		self.pm1 = Label(self.Frame1, textvariable=self.pm1_data, bg="gray7", fg="antique white", font=('Verdana', 20, 'bold'))
		self.pm1_data.set("PM1")
		self.pm1.grid(pady=2)
		self.pm25 = Label(self.Frame1, textvariable=self.pm25_data, bg="gray7", fg="papaya whip", font=('Verdana', 20, 'bold'))
                self.pm25_data.set("PM25")
                self.pm25.grid(pady=2)
		self.pm10 = Label(self.Frame1, textvariable=self.pm10_data, bg="gray7", fg="blanched almond", font=('Verdana', 20, 'bold'))
                self.pm10_data.set("PM10")
                self.pm10.grid(pady=4)

################################################################ FRAME2

		self.temperature = Label(self.Frame2, width=21, textvariable=self.temp_data, bg="gray15", fg="red", font=('Verdana', 20, 'bold'))
		self.temp_data.set("Temperature")
		self.temperature.grid(pady=2)
		self.humidity = Label(self.Frame2, textvariable=self.hum_data, bg="gray15", fg="SteelBlue3", font=('Verdana', 20, 'bold'))
                self.hum_data.set("Humidity")
                self.humidity.grid(pady=2)

		self.time = Label(self.Frame2, textvariable=self.time_data, bg="gray15", fg="lawn green", font=('Verdana', 20, 'bold'))
		self.time_data.set("Time")
		self.time.grid(pady=2)

		self.date = Label(self.Frame2, textvariable=self.date_data, bg="gray15", fg="orange", font=('Verdana', 20, 'bold'))
		self.date_data.set("Date")
		self.date.grid(pady=8)


################################################################ FRAME3

		self.pm = Label(self.Frame3, width=24, height=2, text="Gases", bg="gray37", fg="peach puff", font=('Verdana', 20, 'italic'))
                self.pm.grid(pady=2)

		self.co = Label(self.Frame3, textvariable=self.co_data, bg="gray37", fg="snow", font=('Verdana', 20, 'bold'))
		self.co_data.set("CO")
		self.co.grid(pady=2)

		self.co2 = Label(self.Frame3, textvariable=self.co2_data, bg="gray37", fg="ghost white", font=('Verdana', 20, 'bold'))
                self.co2_data.set("CO2")
                self.co2.grid(pady=2)

		self.no2 = Label(self.Frame3, textvariable=self.no2_data, bg="gray37", fg="white smoke", font=('Verdana', 20, 'bold'))
                self.no2_data.set("NO2")
                self.no2.grid(pady=2)

		self.so2 = Label(self.Frame3, textvariable=self.so2_data, bg="gray37", fg="floral white", font=('Verdana', 20, 'bold'))
                self.so2_data.set("SO2")
                self.so2.grid(pady=2)

		self.o3 = Label(self.Frame3, textvariable=self.o3_data, bg="gray37", fg="linen", font=('Verdana', 20, 'bold'))
		self.o3_data.set("O3")
		self.o3.grid(pady=2)

################################################################# FRAME4

		self.hello = Label(self.Frame4, width=23, height=2, text="DLSU EARTH LAB", bg="grey50", fg="lime green", font=('Verdana', 20, 'bold'))
		self.hello.grid(pady=8)

##################### Init the variables & start measurements ##########################################################################################

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pm1_data = StringVar()
		self.pm25_data = StringVar()
		self.pm10_data = StringVar()
		self.temp_data = StringVar()
		self.hum_data = StringVar()
		self.co_data = StringVar()
		self.co2_data = StringVar()
		self.no2_data = StringVar()
		self.so2_data = StringVar()
		self.o3_data = StringVar()
		self.time_data = StringVar()
		self.date_data = StringVar()
		self.createWidgets()
		self.measure()
		self.grid()
		self.master.title("Air Quality Monitoring System")

##################################### Create and run the GUI ##########################################################################
root = Tk()
app = Application(master=root)
root.geometry("800x400")
app.mainloop()