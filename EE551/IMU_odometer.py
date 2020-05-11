import numpy as np
from math import atan

class IMU_odometer:
	def __init__(self, orientation = [0, 0, 0], v, a):
		#x,y,theta
		self.orientation = orientation
		self.velocity = v
		self.accel = a
	def location(self, sensor, dt)
		e_vec = sensor.euler[0:2]
		e_mag = np.linalg.norm(e_vec)
		u = e_vec/e_mag #heading unit vector
		
		a_vec = sensor.linear_acceleration[0:2]
		a_mag = np.linalg.norm(a_vec)
		a_hd - a_mag*u
		
		v = self.velocity
		
		self.velocity = v +a_hd*dt
		self.orientation[0:2] = self.orientation[0,2] + v*dt +
			0.5*a_hd*dt**2
		self.orientation[2] = atan(e_vec[0]/e_vec[1])
		orientation = self.orientation
		return orientation