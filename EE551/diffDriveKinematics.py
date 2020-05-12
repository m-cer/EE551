from math import cos, sin
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class diffDriveKinematics:
    def __init__(self, l = 10, R = 0.3125, orientation = [0,0,0]):
        self.l = 1
        self.R = R
        #x, y ,theta
        self.orient = orientation
        self.datetime = datetime.now()

    def location(self, duty_l, duty_r):
        dt = (datetime.now() - self.datetime).total_seconds()
        speed = lambda duty: duty*pi*self.R*2*140/60
        vl = speed(duty_l)
        vr = speed(duty_r)
        self.datetime = datetime.now()
        #calculate the new location using
        x, y, theta = self.orient
        if vl != vr:
            R = (self.l/2)*(vl+vr)/(vr-vl)
            omega = (vr-vl)/self.l
            ICC = [x-R*sin(theta),y+R*cos(theta)]

            A = np.array([[cos(omega*dt),-sin(omega*dt),0],
                         [sin(omega*dt), cos(omega*dt),0],
                         [0,0,1]])
            B = np.array([x-ICC[0],y-ICC[1],theta])
            C = np.array([ICC[0],ICC[1],omega*dt])
            #array of x, y, theta
            D = A.dot(B)+C
        else:
            D = [self.orient[0]+vr*dt*cos(theta),
                 self.orient[1]+vr*dt*sin(theta),
                 self.orient[2]]
        self.orient = D
        return D

    def reset(self, l, R, orientation = [0,0,0]):
        self.l = l
        self.R = R
        #x, y ,theta
        self.orient = orientation