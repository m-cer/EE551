import serial
import adafruit_bno055
import logging
#import time
from math import atan, pi


class heading():
	def __init__(self):
		self.uart = serial.Serial("/dev/serial0")
		self.sensor = adafruit_bno055.BNO055_UART(self.uart)
		self.theta = 0
	def get(self):
		try:
			x, y, _ = self.sensor.magnetic
			if y > 0:
				self.theta = 90-atan(x/y)*180./pi
			elif y < 0:
				self.theta = 270 - atan(x/y)*180./pi
			elif y == 0 and x < 0:
				self.theta = 180
			elif y == 0 and x > 0:
				self.theta = 0
		except Exception as e:
			pass
			#likely bus overrun error because of wifi dongle
			#self.uart = serial.Serial("/dev/serial0")
			#self.sensor = adafruit_bno055.BNO055_UART(self.uart)
		return int(abs(self.theta))
