#!/usr/bin/env python3

# Joana Cabrera
# 3/15/2020 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
import matplotlib as mpl
from tube_to_well import *

# TODO: put this into a state machine later
# if layout changes, use lighting location to find A1 and spacing
A1_X = 0.235
A1_Y = 0.59
WELL_SPACING = 0.045
CIRC_RADIUIS  = 0.024

class Well:
	""" A class for individual wells in the matplotlib plot
	"""
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius
		self.circle = Circle(self.center, self.radius, color='gray', zorder=0)
		self.barcode = ''

	def markEmpty(self):
		self.circle.set_color('gray')
		self.circle.zorder=0
		
	def markFilled(self):
		self.circle.set_color('red')
		self.circle.zorder=1

	def markTarget(self):
		self.circle.set_color('yellow')
		self.circle.zorder=2

	def markRescanned(self):
		self.circle.set_color('blue')
		self.circle.zorder=2

class PlateLighting:
	""" A class for lighting up the corresponding well using matplotlib
	"""
	def __init__(self, a1_x, a1_y, circ_radius, well_spacing):

		# set up plot 
		mpl.rcParams['toolbar'] = 'None'
		plt.style.use('dark_background')
		self.fig, self.ax = plt.subplots()
		self.fig.tight_layout()
		self.ax.axis('equal')
		self.fig.subplots_adjust(bottom=0)
		self.ax.axis('off')
		self.well_dict = {} # links barcode to Well object

		# set up tube to well
		self.ttw = TubeToWell()

		# draw all the empty wells
		self.wells = [] # column wise list of wells
		for x in range(12):
			x_coord = a1_x + (well_spacing * x)
			for y in range(8):
				y_coord = a1_y - (well_spacing * y)
				well = Well((x_coord,y_coord), circ_radius)
				self.wells.append(well)
				self.ax.add_artist(well.circle)
		
		# keep track of target index
		self.well_idx = 0


	def switchWell(self, check_input):
		location = self.ttw.checkTubeBarcode(check_input)
		if location:
			self.target = self.wells[self.well_idx]
			self.well_idx += 1
			self.target.markTarget()
			self.target.location = location
			self.target.barcode = check_input
			self.fig.canvas.draw()

			# the well will be marked as filled when the next target is marked 
			self.target.markFilled()

			# link target well object to a barcode in the well_dict dictonary
			self.well_dict[self.target.barcode] = self.target

			return True # return true if new tube

		elif check_input in self.ttw.scanned_tubes:
			already_scanned_tube = self.well_dict[check_input]
			already_scanned_tube.markRescanned()
			self.fig.canvas.draw()
			
			# the well will be marked as filled when the next target is marked 
			already_scanned_tube.markFilled()
			return False # return false if not new tube

	def show(self):
		plt.show()

	def reset(self):
		# mark all wells as empty
		for w in self.wells:
			w.markEmpty()
		self.fig.canvas.draw()

		# clear well dictionary
		self.well_dict.clear()
		self.well_idx = 0

		# reset TubeToWell object
		self.ttw.reset()

# PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING).show()
def main():
	PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING).show()

if __name__== "__main__":
	main()
