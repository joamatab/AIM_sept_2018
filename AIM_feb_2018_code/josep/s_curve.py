# Written by Hayk Gevorgyan
# Jan, 2018
# This script generates bezier curve given two terminal P0 and P3 and radii of curvatures at this points
#
# modified by josep to take input port, output port, and a length

from ipkiss3 import all as i3
import numpy as np
import matplotlib.pyplot as plt

import scipy.optimize as opt


class S_wg(object):
    """

    Properties
        input_port
        output_port
        bend_radius
        LH
            the length of the input straight waveguide section
        N
            ?

    """
    def __init__(self,N=200, input_port=(0.0,0.0),output_port=(6.0,-4.0),bend_radius=(2.),LH=1.0):
        self.input_port = (input_port[0]-0.075,input_port[1])
        self.output_port = (output_port[0]+0.075,output_port[1])
        self.bend_radius = bend_radius
        self.LH=LH
        self.N=N
    def coords(self):

        x1 = np.linspace(self.input_port[0] + self.LH - self.bend_radius, self.input_port[0] + self.LH, self.N)
        x2 = np.linspace(self.input_port[0] + self.LH , self.input_port[0] + self.LH + self.bend_radius, self.N)
        if self.input_port[1]>self.output_port[1] and self.input_port[0]<self.output_port[0] or self.input_port[1]<self.output_port[1] and self.input_port[0]>self.output_port[0] :
            y1 = self.input_port[1]-self.bend_radius+np.sqrt(self.bend_radius**2 - (x1-(self.input_port[0] + self.LH - self.bend_radius))**2)
            y2 = self.output_port[1]+self.bend_radius - np.sqrt(
                self.bend_radius ** 2 - (x2 - (self.input_port[0] + self.LH + self.bend_radius)) ** 2)
            x = np.hstack([ np.array([self.input_port[0],self.input_port[0]+ (self.LH - self.bend_radius)]),x1,x2,np.array([self.output_port[0]])])
            y = np.hstack([ np.array([self.input_port[1],self.input_port[1]]),y1,y2,np.array([self.output_port[1]])])


        elif self.input_port[1]>self.output_port[1] and self.input_port[0]>self.output_port[0] or self.input_port[1]<self.output_port[1] and self.input_port[0]<self.output_port[0]:
            y1 = self.input_port[1]+self.bend_radius-np.sqrt(self.bend_radius**2 - (x1-(self.input_port[0] + self.LH - self.bend_radius))**2)
            y2 = self.output_port[1]-self.bend_radius + np.sqrt(
                self.bend_radius ** 2 - (x2 - (self.input_port[0] + self.LH + self.bend_radius)) ** 2)
            x = np.hstack([ np.array([self.input_port[0], self.input_port[0] + self.LH - self.bend_radius]),x1,x2,np.array([self.output_port[0]])])
            y = np.hstack([ np.array([self.input_port[1], self.input_port[1]]),y1,y2,np.array([self.output_port[1]])])
           # plt.plot(x,y, 'ro')
           # plt.axis('equal')
           # plt.show()
        elif self.input_port[1]==self.output_port[1]:
            x = np.array([self.input_port[0], self.output_port[0]])
            y = np.array([self.input_port[1], self.output_port[1]])



        return np.vstack([x, y]).transpose()
#s=S_wg()
#s.coords()