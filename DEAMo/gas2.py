# Imports
import sys
import datetime
import time
import serial
from Tkinter import *
import tkFont as tkfont
import ttk
import os

# Serial port parameters
serial_speed = 9600
serial_port = '/dev/ttyACM0'

# Test with USB-Serial connection
# serial_port = '/dev/tty.usbmodem1421'
ser = serial.Serial(serial_port, serial_speed)
ser.flushInput()

#Filename
filename = "/home/pi/gas_data/data: " + format(datetime.datetime.now()) + ".txt"
file = open(filename, "w")


############################################################## Main Tkinter application #######################################################
class Application(Frame):

	def shutdown(self):
		os.system("sudo killall python && sudo shutdown -h now")
		
			
########################## Measure data from the sensor
	def measure(self):

		# Request data and read the answer
		ser.write("m")
		time.sleep(.1)
		data = ser.readline()

		# If the answer is not empty, process & display data
		try:

			data = data.strip('\r\n')
			processed_data = data.split(",")
						
			self.pm1_data.set("PM1: " + str(processed_data[0] + " ug/m3"))
			self.pm1.grid()
			self.pm25_data.set("PM2.5: " + str(processed_data[1] + " ug/m3"))
			self.pm25.grid()
			self.pm10_data.set("PM10: " + str(processed_data[2] + " ug/m3"))
			self.pm10.grid()
		
			self.temp_data.set("Temp: " + str(processed_data[3] + " degC"))
			self.temperature.grid()
			self.hum_data.set("Humidity: " + str(processed_data[4] + " %"))
			self.humidity.grid()
		
			self.time_data.set("Time: {:%H:%M:%S} ".format(datetime.datetime.now()))
			self.time.grid()
			self.date_data.set("Date: {:%Y-%m-%d} ".format(datetime.datetime.now()))
			self.date.grid()			

			self.co_data.set("CO: " + str(processed_data[5] + " ppm"))
			self.co.grid()
			self.co2_data.set("CO2: " + str(processed_data[6] + " ppm"))
			self.co2.grid()
			self.no2_data.set("NO2: " + str(processed_data[7] +" ppm"))
			self.no2.grid()
			self.so2_data.set("SO2: " + str(processed_data[8] + " ppm"))
			self.so2.grid()

		except(IndexError, ValueError):
			data = "null"

        	# Wait 1 second between each measurement
                self.after(1000,self.measure)

############################################################## FILEWRITE

		try:

			print(str(processed_data))
			file.write("Time: {:%Y-%m-%d %H:%M:%S}, " .format(datetime.datetime.now()))
			file.write("PM1:" +      str(processed_data[0]) + " ug/m3, " 
				 + "PM2.5:" +    str(processed_data[1]) + " ug/m3, " 
				 + "PM10:" +     str(processed_data[2]) + " ug/m3, "
				 + "Temp:" +     str(processed_data[3]) + " deg C, "
				 + "Humidity:" + str(processed_data[4]) + " % RH, "
				 + "CO:" +       str(processed_data[5]) + " ppm, "
				 + "CO2:" +      str(processed_data[6]) + " ppm, "
				 + "NO2:" +      str(processed_data[7]) + " ppm, "
				 + "SO2:" +      str(processed_data[8]) + " ppm"
                         	 )
			file.write("\r\n")
			file.flush()

		except(IndexError, ValueError):
			data = "null"	
		
############################ Create display elements ######################################################################################
	def createWidgets(self):
		
		#PM FRAME
		self.Frame1 = Frame(self, bg="gray7", borderwidth=10, height=200)
		self.Frame1.grid(  row=0,  column=0,  rowspan=3,      columnspan=2,   sticky=W+E+N+S,  padx=2,  pady=1)
		
		#Temp FRAME
		self.Frame2 = Frame(self, bg="gray15", borderwidth=10, height=200)
                self.Frame2.grid(  row=3,  column=0,   rowspan=3,      columnspan=2,  sticky=W+E+N+S,  padx=2,  pady=1)

		#Gas FRAME
		self.Frame3 = Frame(self, bg="gray37", borderwidth=10, height=300)
                self.Frame3.grid(  row=0,  column=2,   rowspan=4,      columnspan=3,  sticky=W+E+N+S,  padx=2,  pady=1)

		#Time Frame
		self.Frame4 = Frame(self, bg="gray50", borderwidth=10, height=40)
		self.Frame4.grid(  row=4,  column=2,   rowspan=4,      columnspan=3,  sticky=W+E+N+S,  padx=2,  pady=1)
		
############################################################### FRAME1

		self.pm = Label(self.Frame1, text="Particulate Matter", bg="white", fg="black", font=('Verdana', 10, 'italic')) 
		self.pm.grid(pady=1)

		self.pm1 = Label(self.Frame1,  textvariable=self.pm1_data, bg="gray7", fg="white", font=('Verdana', 10, 'bold'))
		self.pm1_data.set("PM1")
		self.pm1.grid(pady=1)		

		self.pm25 = Label(self.Frame1, textvariable=self.pm25_data, bg="gray7", fg="white", font=('Verdana', 10, 'bold'))
                self.pm25_data.set("PM25")
                self.pm25.grid(pady=1)

		self.pm10 = Label(self.Frame1, textvariable=self.pm10_data, bg="gray7", fg="white", font=('Verdana', 10, 'bold'))
                self.pm10_data.set("PM10")
                self.pm10.grid(pady=1)

################################################################ FRAME2

#		self.pm = Label(self.Frame2, text="Temperature", bg="white", fg="black", font=('Verdana', 10, 'italic'))
#               self.pm.grid(pady=1)

		self.temperature = Label(self.Frame2, textvariable=self.temp_data, bg="gray15", fg="red3",       font=('Verdana', 10, 'bold'))
		self.temp_data.set("Temperature")
		self.temperature.grid(pady=1)

		self.humidity = Label(self.Frame2,    textvariable=self.hum_data,  bg="gray15", fg="SteelBlue3", font=('Verdana', 10, 'bold'))
                self.hum_data.set("Humidity")
                self.humidity.grid(pady=1)

################################################################ FRAME3		
		
		self.pm = Label(self.Frame3, text="Gases", bg="white", fg="black", font=('Verdana', 10, 'italic'))
                self.pm.grid(pady=1)

		self.co = Label(self.Frame3,  textvariable=self.co_data,  bg="gray37", fg="white", font=('Verdana', 10, 'bold'))
		self.co_data.set("CO")
		self.co.grid(pady=1)
		
		self.co2 = Label(self.Frame3, textvariable=self.co2_data, bg="gray37", fg="white", font=('Verdana', 10, 'bold'))
                self.co2_data.set("CO2")
                self.co2.grid(pady=1)
		
		self.no2 = Label(self.Frame3, textvariable=self.no2_data, bg="gray37", fg="white", font=('Verdana', 10, 'bold'))
                self.no2_data.set("NO2")
                self.no2.grid(pady=1)
		
		self.so2 = Label(self.Frame3, textvariable=self.so2_data, bg="gray37", fg="white", font=('Verdana', 10, 'bold'))
                self.so2_data.set("SO2")
                self.so2.grid(pady=1)

################################################################# FRAME4

		self.time = Label(self.Frame4, textvariable=self.time_data, bg="gray50", fg="lawn green", font=('Verdana', 10, 'bold'))
		self.time_data.set("Time")
		self.time.grid(pady=1)
		
		self.date = Label(self.Frame4, textvariable=self.date_data, bg="gray50", fg="orange", font=('Verdana', 10, 'bold'))
		self.date_data.set("Date")
		self.date.grid(pady=1)		
		
################################################################## buttons

		self.button1 = Button(self, width = 15, height = 1, text='Shutdown Device', command=self.shutdown, fg='black', bg="light grey")
		self.button1.grid()		

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
		self.time_data = StringVar()
		self.date_data = StringVar()
		self.createWidgets()
		self.measure()
		self.grid()
		self.master.title("Air Quality Sensor")


##################################### Create and run the GUI ##########################################################################
root = Tk()
app = Application(master=root)
root.geometry("320x230")
app.mainloop()
