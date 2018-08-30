# Written by Hayk Gevorgyan
# Jan, 2018
# This script generates bezier curve given two terminal P0 and P3 and radii of curvatures at this points

from ipkiss3 import all as i3
import numpy as np
import scipy.optimize as opt


class BezierCurve(object):
	def __init__(self, N = 1000, P0 = (0.0, 0.0), P1 = (1.0, 0.0), P2 = (1.0, 0.0), P3 = (10.0, 10.0), R = (10.0, 10.0), dy_dx = (0.0, 100000)):
		self.N = N
		self.P0 = P0
		self.P1 = P1
		self.P2 = P2
		self.P3 = P3
		self.R = R
		self.dy_dx = dy_dx
	
	def cont_eqs(self, variables):
		
		(x1, y1, x2, y2) = variables
		f1 = (y1 - self.P0[1])/(x1 - self.P0[0]) - self.dy_dx[0]
		f2 = (self.P3[1] - y2)/(self.P3[0] - x2) - self.dy_dx[1]
		f3 = (3.0/2.0)*( (x1 - self.P0[0])**2.0 + (y1 - self.P0[1])**2.0 )**(3.0/2.0)/( (x1 - self.P0[0])*(y2-2.0*y1+self.P0[1]) - (y1 - self.P0[1])*(x2-2.0*x1+self.P0[0]) ) - self.R[0]
		f4 = (3.0/2.0)*( (self.P3[0] - x2)**2.0 + (self.P3[1] - y2)**2.0 )**(3.0/2.0)/( (self.P3[0] - x2)*(self.P3[1]-2.0*y2+y1) - (self.P3[1] - y2)*(self.P3[0]-2.0*x2+x1) ) - self.R[1]

		return [f1, f2, f3, f4]
	
	def find_knobs(self):
		solution  = opt.fsolve( self.cont_eqs, (self.P1[0], self.P1[1], self.P2[0], self.P2[1]), xtol=1e-20)
		# self.P1 = (solution[0], solution[1])
		# self.P2 = (solution[2], solution[3])
		return solution
		
	def bezier_coords(self):
		t = np.linspace(0.0, 1.0, self.N)
		B_x = []
		B_y = []
		B = []
		solution = self.find_knobs()
		self.P1 = (solution[0], solution[1])
		self.P2 = (solution[2], solution[3])
		for ii in range(len(t)):
			B_x.append((1.0 - t[ii])**3.0*self.P0[0] + 3.0*(1.0-t[ii])**2.0*t[ii]*self.P1[0] + 3.0*(1.0-t[ii])*t[ii]**2.0*self.P2[0] + t[ii]**3.0*self.P3[0])
			B_y.append((1.0 - t[ii])**3.0*self.P0[1] + 3.0*(1.0-t[ii])**2.0*t[ii]*self.P1[1] + 3.0*(1.0-t[ii])*t[ii]**2.0*self.P2[1] + t[ii]**3.0*self.P3[1])
			B.append((B_x[ii], B_y[ii]))
		
		return B