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
air=g3.g3sensor()

# Serial port parameters Arduino Mega
mega_serial_speed = 9600
mega_serial_port = '/dev/ttyACM0'
mega_ser = serial.Serial(mega_serial_port, mega_serial_speed)
mega_ser.flushInput()

# Serial port parameters Arduino Uno
auno_serial_speed = 9600
auno_serial_port = '/dev/ttyUSB0'
auno_ser = serial.Serial(auno_serial_port, auno_serial_speed)
auno_ser.flush

#Filename
filename = "/home/pi/Desktop/AQMS(" + "{:%H:%M %m-%d-%Y})".format(datetime.datetime.now()) + ".txt"
file = open(filename, "w")
file.write("Time,PM1,PM2.5,PM10,Temp,Hum,NO2,O3,CO2,SO2,CO\n")

#Proxy Handler
#proxy = 'http://proxy.dlsu.edu.ph:80'

#os.environ['http_proxy'] = proxy 
#os.environ['HTTP_PROXY'] = proxy
#os.environ['https_proxy'] = proxy
#os.environ['HTTPS_PROXY'] = proxy

# Webserver
SERVER_URL = "http://weather.pogznet.com/index.php"
API_ENDPOINT = "/API/data_add?"
SEID = ""
SKEY = ""
BASE_URL = SERVER_URL+API_ENDPOINT \
	+ "seid=" + SEID \
	+ "&skey=" + SKEY

############################################################## Main Tkinter application #######################################################

class Application(Frame):

	def measure(self):

		# Request data from pm3003
		try:
			pmdata=air.read("/dev/ttyAMA0") #pms3003
		except:
			pmdata=[0,0,0,0,0,0]

		# Request data and read the answer of 2 arduino
		mega_ser.write("m")
		time.sleep(.1)
		mega_data = mega_ser.readline()

		auno_ser.write("m")
		time.sleep(.1)
		auno_data = auno_ser.readline()


		# If the answer is not empty, process & display data
		try:
			# Get arduino mega data
			mega_data = mega_data.strip('\r\n')
			mega_processed_data = mega_data.split(",")

			# Get arduino uno data
			auno_data = auno_data.strip('\r\n')
			auno_processed_data = auno_data.split(",")

			# Initialize data
			pm01 = str(pmdata[3])
			pm25 = str(pmdata[5])
			pm10 = str(pmdata[4])
			temp = str(mega_processed_data[0])
			humi = str(mega_processed_data[1])
			no2x = str(mega_processed_data[2])
			o3xx = str(mega_processed_data[3])
			co2x = str(mega_processed_data[4])
			so2x = str(auno_processed_data[0])
			coxx = str(auno_processed_data[1])

			# Save to a text file
			file.write("{:%Y-%m-%d %H:%M:%S},".format(datetime.datetime.now()))
			file.write(pm01 + ","
				+ pm25 + ","
				+ pm10 + ","
				+ temp + ","
				+ humi + ","
				+ no2x + ","
				+ o3xx + ","
				+ co2x + ","
				+ so2x + ","
				+ coxx)
			file.write("\r\n")
			file.flush()

			# Try sending to webserver
			try:

				VAL_time = str(int(time.time()))
				HTTP_REQUEST = BASE_URL	+ "&time=" + VAL_time \
					+ "&pm01=" + pm01 \
					+ "&pm25=" + pm25 \
					+ "&pm10=" + pm10 \
					+ "&temp=" + temp \
					+ "&humi=" + humi \
					+ "&no2x=" + no2x \
					+ "&ozne=" + o3xx \
					+ "&co2x=" + co2x \
					+ "&so2x=" + so2x \
					+ "&coxx=" + coxx 
				c = pycurl.Curl()
				c.close()
				sendbuff = StringIO()
				s = pycurl.Curl()
				s.setopt(c.URL, HTTP_REQUEST)
				s.setopt(c.WRITEDATA, sendbuff)
				s.perform()
				s.close()
				req_result = sendbuff.getvalue()
			except:
				pass

			# Initialize to GUI
			self.time_data.set( "Time: {:%H:%M}    ".format(datetime.datetime.now()))
			self.date_data.set( "Date: {:%Y-%m-%d} ".format(datetime.datetime.now()))

			self.temp_data.set( "Temp: " + temp + " degC" )
			self.humi_data.set( "Humi: " + humi + " %%"   )
			self.no2x_data.set( "NO2 : " + no2x + " ppm"  )
			self.o3xx_data.set( "O3  : " + o3xx + " ppm"  )
			self.co2x_data.set( "CO2 : " + co2x + " ppm"  )

			self.so2x_data.set( "SO2 : " + so2x + " ppm"  )
			self.coxx_data.set( "CO  : " + coxx + " ppm"  )

			self.pm01_data.set( "PM1 : " + pm01 + " ug/m3")
			self.pm25_data.set("PM2.5: " + pm25 + " ug/m3")
			self.pm10_data.set( "PM10: " + pm10 + " ug/m3")

		except(IndexError, ValueError):
			pass

        	# Wait 1 second between each measurement
                self.after(1000,self.measure)

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


		self.pm01 = Label(self.Frame1, textvariable=self.pm01_data, bg="gray7", fg="antique white",   font=('Verdana', 20, 'bold'))
		self.pm01_data.set("PM1")
		self.pm01.grid(pady=2)

		self.pm25 = Label(self.Frame1, textvariable=self.pm25_data, bg="gray7", fg="papaya whip",     font=('Verdana', 20, 'bold'))
                self.pm25_data.set("PM25")
                self.pm25.grid(pady=2)

		self.pm10 = Label(self.Frame1, textvariable=self.pm10_data, bg="gray7", fg="blanched almond", font=('Verdana', 20, 'bold'))
                self.pm10_data.set("PM10")
                self.pm10.grid(pady=4)

################################################################ FRAME2

		self.temperature = Label(self.Frame2, width=21, textvariable=self.temp_data, bg="gray15", fg="red", font=('Verdana', 20, 'bold'))
		self.temp_data.set("Temperature")
		self.temperature.grid(pady=2)

		self.humidity = Label(self.Frame2, textvariable=self.humi_data, bg="gray15", fg="SteelBlue3", font=('Verdana', 20, 'bold'))
                self.humi_data.set("Humidity")
                self.humidity.grid(pady=2)

		self.time = Label(self.Frame2, textvariable=self.time_data, bg="gray15", fg="lawn green", font=('Verdana', 20, 'bold'))
		self.time_data.set("Time")
		self.time.grid(pady=2)

		self.date = Label(self.Frame2, textvariable=self.date_data, bg="gray15", fg="orange", font=('Verdana', 20, 'bold'))
		self.date_data.set("Date")
		self.date.grid(pady=8)


################################################################ FRAME3

		self.pm2 = Label(self.Frame3, width=21, height=2, text="Gases", bg="gray37", fg="peach puff", font=('Verdana', 20, 'italic'))
                self.pm2.grid(pady=2)


		self.coxx = Label(self.Frame3, textvariable=self.coxx_data, bg="gray37", fg="snow", font=('Verdana', 20, 'bold'))
		self.coxx_data.set("CO")
		self.coxx.grid(pady=2)

		self.co2x = Label(self.Frame3, textvariable=self.co2x_data, bg="gray37", fg="ghost white", font=('Verdana', 20, 'bold'))
                self.co2x_data.set("CO2")
                self.co2x.grid(pady=2)

		self.no2x = Label(self.Frame3, textvariable=self.no2x_data, bg="gray37", fg="white smoke", font=('Verdana', 20, 'bold'))
                self.no2x_data.set("NO2")
                self.no2x.grid(pady=2)

		self.so2x = Label(self.Frame3, textvariable=self.so2x_data, bg="gray37", fg="floral white", font=('Verdana', 20, 'bold'))
                self.so2x_data.set("SO2")
                self.so2x.grid(pady=2)

		self.o3xx = Label(self.Frame3, textvariable=self.o3xx_data, bg="gray37", fg="linen", font=('Verdana', 20, 'bold'))
		self.o3xx_data.set("O3")
		self.o3xx.grid(pady=2)

################################################################# FRAME4

		self.hello = Label(self.Frame4, width=21, height=2, text="DLSU EARTH", bg="grey50", fg="dark green", font=('Verdana', 20, 'bold'))
		self.hello.grid(pady=10)

##################### Init the variables & start measurements ##########################################################################################

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pm01_data = StringVar()
		self.pm25_data = StringVar()
		self.pm10_data = StringVar()
		self.temp_data = StringVar()
		self.humi_data = StringVar()
		self.coxx_data = StringVar()
		self.co2x_data = StringVar()
		self.no2x_data = StringVar()
		self.so2x_data = StringVar()
		self.o3xx_data = StringVar()
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
