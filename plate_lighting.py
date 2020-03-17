#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
import matplotlib as mpl
from tube_to_well import *

# put this into a state machine later
# if layout changes, use lighting location to find A1 and spacing
A1_X = 0.23
A1_Y = 0.435
WELL_SPACING = 0.045
CIRC_RADIUIS  = 0.023


class Well:
	def __init__(self, center, radius):
		self.target = False
		self.center = center
		self.radius = radius
		self.circle = Circle(self.center, self.radius, color='gray', zorder=0)
		self.barcode = ''

	def markEmpty(self):
		self.target = False
		self.circle.set_color('gray')
		

	def markFilled(self):
		self.target = False
		self.circle.set_color('red')
		

	def markTarget(self):
		self.target = True
		self.circle.set_color('yellow')
		self.circle.zorder=1

	def markRescanned(self):
		self.target = False
		self.circle.set_color('blue')
		self.circle.zorder=2

class PlateLighting:
	def __init__(self, a1_x, a1_y, circ_radius, well_spacing):

		# set up plot 
		mpl.rcParams['toolbar'] = 'None'
		plt.style.use('dark_background')
		self.fig, self.ax = plt.subplots()
		self.fig.tight_layout()
		self.ax.axis('equal')
		self.fig.subplots_adjust(bottom=0)
		self.ax.axis('off')
		self.fig.canvas.manager.full_screen_toggle() # make sure to set the well lighting display as the main display (go to windows display setting)
		self.well_dict = {}

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
		self.wells_iterator = iter(self.wells)

		self.check_input = ''
		self.fig.canvas.mpl_connect('key_press_event', self.on_trigger)

	def on_trigger(self, event):
		# compile the full barcode onto check_input
		if event.key != 'enter':
			self.check_input += event.key
		if event.key == 'enter':
			# check if it was a valid barcode (either have all the accessed barcodes or make sure input comes from a barcode scanner)
			if self.ttw.checkBarcode(self.check_input):
				target = next(self.wells_iterator)
				target.markTarget()
				target.barcode = self.check_input
				self.fig.canvas.draw()

				# the well will be marked as filled when the next target is marked 
				target.markFilled()
				target.barcode = self.check_input
				
				self.well_dict[target.barcode] = target

			elif self.check_input in self.ttw.scanned_tubes:
				already_scanned_tube = self.well_dict[self.check_input]
				print(already_scanned_tube)
				already_scanned_tube.markRescanned()
				self.fig.canvas.draw()
				
				# the well will be marked as filled when the next target is marked 
				already_scanned_tube.markFilled()

			self.check_input = ''

	def show(self):
		plt.show()


# PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING).show()
def main():
	PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING).show()

if __name__== "__main__":
	main()
