import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time
import matplotlib as mpl

# put this into a state machine later
# if layout changes, use lighting location to find A1 and spacing
A1_X = 0.23
A1_Y = 0.41
WELL_SPACING = 0.045
CIRC_RADIUIS  = 0.025


class WellCircle:
	def __init__(self, center, radius):
		self.empty = True
		self.target = False
		self.center = center
		self.radius = radius
		self.circle = Circle(self.center, self.radius, color='blue', zorder=0)

	def markEmpty(self):
		self.empty = True
		self.target = False
		self.circle.set_color('blue')
		# return self.circle

	def markFilled(self):
		self.empty = False
		self.target = False
		self.circle.set_color('red')
		# return self.circle

	def markTarget(self):
		self.target = True
		self.circle.set_color('yellow')
		self.circle.zorder=1
		# return self.circle

class PlateLighting:
	def __init__(self, a1_x, a1_y, circ_radius, well_spacing):

		# set up plot 
		mpl.rcParams['toolbar'] = 'None'
		plt.style.use('dark_background')
		self.fig, self.ax = plt.subplots()
		self.fig.tight_layout()
		self.ax.axis('equal')
		self.ax.axis('off')
		self.fig.canvas.manager.full_screen_toggle() # make sure to set the well lighting display as the main display (go to windows display setting)

		# draw all the empty wells
		self.wells = [] # column wise list of wells
		for x in range(12):
			x_coord = a1_x + (well_spacing * x)
			for y in range(8):
				y_coord = a1_y - (well_spacing * y)
				well = WellCircle((x_coord,y_coord), circ_radius)
				self.wells.append(well)
				self.ax.add_artist(well.circle)
		self.wells_iterator = iter(self.wells)

		self.fig.canvas.mpl_connect('key_press_event', self.on_trigger)

	def on_trigger(self, event):
		if event.key == 'enter':
			target = next(self.wells_iterator)
			target.markTarget()
			self.fig.canvas.draw()
			target.markFilled()

	def show(self):
		plt.show()


PlateLighting(A1_X, A1_Y, CIRC_RADIUIS, WELL_SPACING).show()