from math import cos, sin
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


vl = 10. #left cm/s
vr = 6. #right cm/s


class diffDriveKinematics:
	def __init__(self, l = 10, R = 0.3125, orientation = [0,0,0]):
		self.l = l
		self.R = R
		#x, y ,theta
		self.orient = orientation
		self.datetime = datetime.now()

	def location(self, vl, vr):
		dt = datetime.now() - self.datetime
		#calculate the new location using
		x = self.orient[0]
		y = self.orient[1]
		theta = self.orient[2]
		R = (self.l/2)*(vl+vr)/(vr-vl)
		omega = (vr-vl)/l
		ICC = [x-R*sin(theta),y+R*cos(theta)]
		
		A = np.array([[cos(omega*dt),-sin(omega*dt.total_seconds()),0],
             [sin(omega*dt), cos(omega*dt),0],
             [0,0,1]])
		B = np.array([x-ICC[0],y-ICC[1],theta])
		C = np.array([ICC[0],ICC[1],omega*dt])
		#array of x, y, theta
		D = A.dot(B)+C
		self.orient = D
		return D

	def reset(self, l, R, orientation = [0,0,0]):
		self.l = l
		self.R = R
		#x, y ,theta
		self.orient = orientation
		

dt = 0.01
tmax = 100
trange = int(tmax/dt)

D = diffDriveKinematics(orientation = [0,0,0])

X = [orientation[0]]
Y = [orientation[1]]
for each in range(trange):
    D = diffDriveKinematics.location(vl,vr)
    X.append(D[0])
    Y.append(D[1])
plt.plot(X,Y)
plt.axes().set_aspect('equal','box')
plt.show()