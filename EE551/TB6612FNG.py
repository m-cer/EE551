from gpiozero import output_devices
from gpiozero.exc import OutputDeviceBadValue, GPIOPinMissing
from gpiozero.devices import CompositeDevice
from gpiozero.mixins import SourceMixin
from gpiozero.output_devices import DigitalOutputDevice, PWMOutputDevice
from collections import OrderedDict

from time import sleep


class TB6612FNG(SourceMixin, CompositeDevice):
	def __init__(self, output_one = None, output_two = None, pwm = None,
					enable = None, pin_factory = None):
		if not all (p is not None for p in [output_one, output_two, pwm]):
			raise GPIOPinMissing(
				'output_one, output_two, and pwm must be provided'
				)
		devices = OrderedDict((
			('output_one_device', DigitalOutputDevice(output_one)),
			('output_two_device', DigitalOutputDevice(output_two)),
			('pwm_device', PWMOutputDevice(pwm)),
		))
		if enable is not None:
			devices['enable_device'] = DigitalOutputDevice(enable,
														   initial_value = True)
		super(TB6612FNG, self).__init__(_order=devices.keys(), **devices)

	@property
	def value(self):
		return self.pwm_device.value
		
	@value.setter
	def value(self, value):
		if not -1 <= value <= 1:
			raise OutputDeviceBadValue("Value must be between -1 and 1")
		if value > 0:
			try:
				self.forward(value)
			except ValueError as e:
				raise OutputDeviceBadValue(e)
		elif value < 0:
			try:
				self.backward(abs(value))
			except ValueError as e:
				raise OutputDeviceBadValue(e)
		else:
			self.stop()
			
	@property
	def is_active(self):
		return self.value != 0
	
	def forward(self,speed = 1):
		if not 0 <= speed <= 1:
			raise ValueError('Forward speed must be between 0 and 1')
		self.output_one_device.on()
		self.output_two_device.off()
		self.pwm_device.value = speed
	
	def backward(self,speed = 1):
		if not 0 <= abs(speed) <= 1:
			raise ValueError('Backward speed must be between 0 and 1')
		self.output_one_device.off()
		self.output_two_device.on()
		self.pwm_device.value = speed
		
	def reverse(self):
		self.value = -self.value
	
	def short_brake(self)
		self.output_one_device.on()
		self.output_two_device.on()
	
	def stop(self):
		self.output_one_device.off()
		self.output_two_device.off()
		self.pwm_device.value = 1

#test
def motor_test():
	A = TB6612FNG(output_one = 'GPIO27', output_two = 'GPIO17', pwm = 'GPIO12')
	B = TB6612FNG(output_one = 'GPIO5', output_two = 'GPIO6', pwm = 'GPIO13')
	A.forward(1)
	B.forward(1)
	sleep(5)
	A.reverse()
	B.reverse()
	sleep(5)
	A.stop()
	B.stop()
